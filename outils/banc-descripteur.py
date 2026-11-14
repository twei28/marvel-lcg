#!/usr/bin/env python3
"""Banc du DESCRIPTEUR DE MONDE : temps, profil et empreinte, sans reseau.

Cree le 20/10/2026 (backlog 22, « tenir plus de joueurs »). Le banc de charge
(`outils/charge-serveur.py`) mesure la machine entiere : sur une machine
partagee, ses latences disent surtout ce que font les AUTRES processus. Ce banc
joue une partie complete dans un seul processus, au pilote de
`tools/autoplay.py` (graine fixee, donc rejouable a l'identique), et mesure
uniquement ce que coute le descripteur :

  * a chaque rendu (`WorldRender.PresentInternal`), le moteur reconstruit le
    descripteur et l'enregistre (« Revoir sa partie ») ;
  * a chaque rendu, on simule ce que fait la route `/get_world` pour DEUX
    clients : l'hote en siege partage (monde complet, sans masque) et un
    joueur au siege 0 (monde masque) — `MasquerCeQuOnNaPasLeDroitDeVoir`
    puis `Json.DumpGZip`, les vraies fonctions du serveur.

Modes :
  temps     temps CPU total, et part de chaque etape (rendu, /get_world) ;
  profil    cProfile de toute la partie (fichier .prof, lisible par pstats) ;
  empreinte une ligne par rendu : sha256 du JSON servi par /get_world (non
            masque et masque siege 0) ET du dictionnaire enregistre. Deux
            versions du moteur sont equivalentes si les fichiers sont
            identiques octet pour octet.

Usage (depuis la racine du depot, Python 3.10) :
    python3.10 outils/banc-descripteur.py --mode temps --deck spider_man \\
        --vilain rhino --graine 1 --sortie /tmp/banc.json

Le processus se termine par os._exit (comme autoplay) : une partie par appel.
"""
import argparse
import hashlib
import json
import os
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JEU = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
GAME_SRC = os.path.join(JEU, ".game-src")


def identiques(a, b):
    """Egalite stricte : meme type exact a chaque noeud, memes valeurs, meme ordre des cles."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a.keys()) == list(b.keys()) and all(identiques(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(identiques(x, y) for x, y in zip(a, b))
    return a == b


def masque_reference(asdict, descriptor, autorises):
    """Le masque de `/get_world` AVANT le backlog 22, recopie tel quel de
    server_sync.py (`asdict` puis second parcours `masquer`). Sert de temoin."""
    brut = asdict(descriptor)

    def masquer(noeud) -> None:
        if isinstance(noeud, dict):
            vus = noeud.get('visible_for_players')
            if isinstance(vus, list) and 'name' in noeud and not (set(vus) & autorises):
                noeud['name'] = ''
                noeud['card_id'] = ''
                noeud['pic_id'] = ''
                noeud['card_type'] = ''
                noeud['traits'] = {}
                noeud['info'] = {}
                noeud['buffs'] = {}
                noeud['cost'] = 0
            for valeur in noeud.values():
                masquer(valeur)
        elif isinstance(noeud, list):
            for valeur in noeud:
                masquer(valeur)

    masquer(brut)
    return brut


def principal():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("temps", "profil", "empreinte"), default="temps")
    ap.add_argument("--deck", default="spider_man", help="deck de depart, ou a+b pour deux joueurs")
    ap.add_argument("--vilain", default="rhino")
    ap.add_argument("--difficulte", default="normal")
    ap.add_argument("--profil-pilote", default="equilibre")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--reference", action="store_true",
                    help="rejouer le moteur d'AVANT le backlog 22 (asdict standard, masque en deux passes)")
    a = ap.parse_args()

    sys.path.insert(0, os.path.join(JEU, "tools"))
    import autoplay  # noqa: E402  (n'importe rien du moteur a l'import)

    # Le moteur est importe depuis .game-src (liens vers src/), comme autoplay.
    sys.path.insert(0, GAME_SRC)
    os.chdir(GAME_SRC)
    os.environ.setdefault("RELEASE", "1")

    # Meme ordre d'import qu'autoplay (le moteur a des imports circulaires).
    from engine.device.manager.base import DeviceManager  # noqa: F401
    from game.world.world_render import WorldRender
    from engine.lib import Json
    from engine.device.web.server.server_sync import GameServerSync

    class FauxServeur:
        """Juste ce qu'il faut a MasquerCeQuOnNaPasLeDroitDeVoir : un client
        qui tient le siege 0 (joueur ordinaire, sans siege partage)."""
        def sieges_visibles(self, request):
            return {0}

    faux = FauxServeur()
    mesures = {"rendus": 0, "present_s": 0.0, "monde_s": 0.0, "octets_gzip": 0}
    sortie_empreinte = open(a.sortie, "w") if a.mode == "empreinte" else None

    # Le dictionnaire enregistre (« Revoir sa partie ») : capture a la source.
    from engine import enregistrement as module_enregistrement
    rendu_original = module_enregistrement.Enregistrement.Rendu.__func__
    dernier_enregistre = {"d": None}

    def rendu_espion(cls, partie, monde, entete, ressources=None):
        dernier_enregistre["d"] = monde
        return rendu_original(cls, partie, monde, entete, ressources)
    module_enregistrement.Enregistrement.Rendu = classmethod(rendu_espion)

    # Ventilation du temps : construction du descripteur, et conversion en
    # dictionnaire (`dataclasses.asdict`, appele par l'enregistrement et par
    # le masque). Les deux appelants importent `asdict` A L'APPEL : remplacer
    # l'attribut du module suffit.
    from game.render.to_descriptor import ToDescriptor
    import dataclasses
    world_original = ToDescriptor.World
    asdict_original = dataclasses.asdict
    mesures.update({"construction_s": 0.0, "asdict_s": 0.0, "asdict_n": 0})

    def world_mesure(*args, **kwargs):
        t = time.process_time()
        try:
            return world_original(*args, **kwargs)
        finally:
            mesures["construction_s"] += time.process_time() - t

    def asdict_mesure(obj, *args, **kwargs):
        t = time.process_time()
        try:
            return asdict_original(obj, *args, **kwargs)
        finally:
            mesures["asdict_s"] += time.process_time() - t
            mesures["asdict_n"] += 1

    ToDescriptor.World = staticmethod(world_mesure)
    dataclasses.asdict = asdict_mesure
    # Sa remplacante (backlog 22), si cette version du moteur l'a.
    try:
        from engine.lib import en_dict
        # --reference : rejouer le moteur d'AVANT (asdict standard), pour une
        # mesure avant/apres entrelacee sur une machine a charge variable.
        rapide_original = asdict_original if a.reference else en_dict.asdict_rapide

        def rapide_mesure(obj):
            t = time.process_time()
            try:
                return rapide_original(obj)
            finally:
                mesures["asdict_s"] += time.process_time() - t
                mesures["asdict_n"] += 1
        en_dict.asdict_rapide = rapide_mesure
        if a.reference and hasattr(en_dict, "asdict_masque"):
            en_dict.asdict_masque = lambda obj, autorises: masque_reference(asdict_original, obj, autorises)
    except ImportError:
        pass

    present_original = WorldRender.PresentInternal

    def present_mesure(self, *args, **kwargs):
        avant = self.descriptor
        t0 = time.process_time()
        resultat = present_original(self, *args, **kwargs)
        t1 = time.process_time()
        mesures["present_s"] += t1 - t0
        if self.descriptor is avant:
            return resultat  # rendu saute (skip) : rien de neuf a servir
        mesures["rendus"] += 1
        # Ce que /get_world sert, deux clients : siege partage, puis siege 0.
        t2 = time.process_time()
        brut = Json.DumpGZip(self.descriptor)
        masque = Json.DumpGZip(GameServerSync.MasquerCeQuOnNaPasLeDroitDeVoir(faux, self.descriptor, None))
        mesures["monde_s"] += time.process_time() - t2
        mesures["octets_gzip"] += len(brut) + len(masque)
        if sortie_empreinte is not None:
            # L'empreinte porte sur le JSON (le gzip embarque une date).
            j_brut = Json.Dumps(self.descriptor).encode("utf-8")
            j_masque = Json.Dumps(GameServerSync.MasquerCeQuOnNaPasLeDroitDeVoir(faux, self.descriptor, None)).encode("utf-8")
            enr = dernier_enregistre["d"]
            j_enr = json.dumps(enr, sort_keys=False).encode("utf-8") if enr is not None else b""
            dernier_enregistre["d"] = None
            # Controle strict de `asdict_rapide` contre la bibliotheque standard :
            # memes types (une liste n'est pas un tuple, meme si le JSON les confond)
            # et memes valeurs, noeud par noeud.
            # Idem pour le masque en une passe, contre le temoin d'avant, pour
            # les deux sieges et pour un siege qui n'existe pas.
            try:
                from engine.lib.en_dict import _interne as rapide, _interne_masque
                ok = identiques(rapide(self.descriptor), asdict_original(self.descriptor))
                for autorises in ({0}, {1}, {7}):
                    ok = ok and identiques(_interne_masque(self.descriptor, autorises, True),
                                           masque_reference(asdict_original, self.descriptor, autorises))
                strict = "strict-ok" if ok else "STRICT-DIFFERENT"
            except ImportError:
                strict = "strict-sans-objet"
            sortie_empreinte.write("%d %s %s %s %d %s\n" % (
                self.descriptor.render_id,
                hashlib.sha256(j_brut).hexdigest(),
                hashlib.sha256(j_masque).hexdigest(),
                hashlib.sha256(j_enr).hexdigest(),
                len(j_brut), strict))
            sortie_empreinte.flush()
        return resultat

    WorldRender.PresentInternal = present_mesure

    profileur = None
    if a.mode == "profil":
        import cProfile
        profileur = cProfile.Profile()

    debut_cpu = time.process_time()
    debut_mur = time.time()
    exit_original = os._exit

    def fin(code=0):
        total = time.process_time() - debut_cpu
        if profileur is not None:
            profileur.disable()
            profileur.dump_stats(a.sortie)
        if a.mode == "temps":
            r = dict(mesures)
            r.update({"cpu_total_s": round(total, 3), "mur_s": round(time.time() - debut_mur, 1),
                      "deck": a.deck, "vilain": a.vilain, "graine": a.graine})
            for k in ("present_s", "monde_s", "construction_s", "asdict_s"):
                r[k] = round(r[k], 3)
            with open(a.sortie, "w") as f:
                json.dump(r, f)
        if sortie_empreinte is not None:
            sortie_empreinte.close()
        exit_original(code)

    os._exit = fin
    if profileur is not None:
        profileur.enable()
    resultat = os.path.join(os.path.dirname(os.path.abspath(a.sortie)),
                            "autoplay-%s-%s-%d.json" % (a.deck.replace("+", "_"), a.vilain, a.graine))
    autoplay.jouer_une_partie(GAME_SRC, 0, a.deck, a.vilain, a.difficulte, a.profil_pilote,
                              a.graine, resultat, 0)


if __name__ == "__main__":
    principal()
