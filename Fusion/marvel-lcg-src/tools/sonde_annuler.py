"""SONDE D'ANNULATION : l'instantane remet-il VRAIMENT toute la partie en place ?  (16/11/2026)

Message d'un joueur / de l'utilisateur : « l'annuler, ca bug un peu apres ». Un instantane restaure le contenu des objets qu'il a
atteints ; tout ce qu'il n'atteint pas (attribut de classe, globale de module, objet cree puis rattache ailleurs) reste faux, et ca ne se voit
que quelques coups plus tard. Cette sonde le mesure, sur de VRAIES parties jouees par le pilote automatique :

  question du tour k      : (planifiee) on prend une REFERENCE : un instantane du monde + une photo des globales de modules et des attributs de classe ;
  question du tour k + 1  : le pilote vient de jouer UNE action ; la sonde demande l'annulation (comme `Cheat.do_undo`) ;
  question du tour k (re-posee) : on compare l'etat a la reference. Tout ecart est un defaut de restauration.

Les ecarts sont ecrits dans /tmp/sonde_annuler_<etiquette>.json et listes dans le journal de la partie (`SONDE ...`).
Branchement : `AUTOPLAY_SONDE_ANNULER=1 python tools/autoplay.py ...` (voir le crochet dans `jouer_une_partie`).
"""
import json
import os
import random
import sys
import types

# Une annulation sur deux questions du tour eligibles, par defaut. Reglable : AUTOPLAY_SONDE_PROBA (0 a 1).
PROBA = float(os.environ.get("AUTOPLAY_SONDE_PROBA", "0.5"))
MAX_ECARTS_PAR_ANNULATION = 25


# ------------------------------------------------------------------ globales
def _modules_du_jeu():
    for nom, mod in list(sys.modules.items()):
        if mod is None or not isinstance(mod, types.ModuleType):
            continue
        if nom.split(".", 1)[0] in ("game", "cards", "core"):
            yield nom, mod


def _copie_superficielle(v):
    if isinstance(v, dict):
        return ("dict", dict(v))
    if isinstance(v, list):
        return ("list", list(v))
    if isinstance(v, set):
        return ("set", set(v))
    return None


def photo_globales():
    """Les conteneurs mutables des modules du jeu ET des attributs de classe : ce que l'instantane ne voit pas (`game.*`, `cards.*`)."""
    photo = {}
    for nom, mod in _modules_du_jeu():
        for cle, val in list(vars(mod).items()):
            if cle.startswith("__"):
                continue
            c = _copie_superficielle(val)
            if c is not None:
                photo[("module", nom, cle)] = (val, c)
            elif isinstance(val, type) and getattr(val, "__module__", "") == nom:
                for ck, cv in list(vars(val).items()):
                    if ck.startswith("__"):
                        continue
                    cc = _copie_superficielle(cv)
                    if cc is not None:
                        photo[("classe", f"{nom}.{val.__name__}", ck)] = (cv, cc)
    return photo


def ecarts_globales(avant, apres):
    ecarts = []
    for cle, (objet, (genre, copie)) in avant.items():
        if cle not in apres or "instantane" in cle[1]:  # le cache de types de l'instantane lui-meme grossit : sans importance
            continue
        (objet2, (genre2, copie2)) = apres[cle]
        if objet is not objet2:
            ecarts.append(f"GLOBALE {cle[0]} {cle[1]}.{cle[2]} : l'objet a ete REMPLACE")
        elif genre == "dict":
            if set(copie) != set(copie2) or any(copie[k] is not copie2[k] and copie[k] != copie2[k] for k in copie):
                ecarts.append(f"GLOBALE {cle[0]} {cle[1]}.{cle[2]} : dict {len(copie)} -> {len(copie2)} entrees")
        elif genre == "list":
            if len(copie) != len(copie2) or any(a is not b and a != b for a, b in zip(copie, copie2)):
                ecarts.append(f"GLOBALE {cle[0]} {cle[1]}.{cle[2]} : liste {len(copie)} -> {len(copie2)} elements")
        elif copie != copie2:
            ecarts.append(f"GLOBALE {cle[0]} {cle[1]}.{cle[2]} : ensemble {len(copie)} -> {len(copie2)} elements")
    for cle in apres:
        if cle not in avant:
            ecarts.append(f"GLOBALE {cle[0]} {cle[1]}.{cle[2]} : conteneur apparu depuis la reference")
    return ecarts


# ------------------------------------------------------------------ graphe
def _court(v, n=70):
    try:
        t = repr(v)
    except Exception:
        t = f"<{type(v).__name__}>"
    return t if len(t) <= n else t[: n - 1] + "…"


def _egal(a, b):
    """Meme valeur ? Identite d'abord ; puis egalite pour les conteneurs ET les atomes (un cache de rendu comme `crc` est RECREE a chaque
    lecture : un dict neuf et egal n'est pas un defaut de restauration)."""
    if a is b:
        return True
    if type(a) is not type(b):
        return False
    try:
        if isinstance(a, (dict, list, set, frozenset, tuple, int, float, str, bytes, bool, complex)):
            return bool(a == b)
    except Exception:
        return False
    return False


def comparer_instantanes(ref, now):
    """Ecarts entre deux Instantane pris sur le MEME graphe : meme objet, contenu different = restauration incomplete."""
    from game.world import instantane as I
    ecarts = []
    a = {id(o): (g, o, s) for g, o, s in ref.entrees}
    b = {id(o): (g, o, s) for g, o, s in now.entrees}
    for i, (g, o, s) in a.items():
        if i not in b:
            if type(o).__name__ not in ("dict", "list", "set", "deque"):  # un conteneur neuf remplace son jumeau egal : sans importance
                ecarts.append(f"OBJET {type(o).__name__} atteignable a la reference, plus maintenant")
            continue
        g2, o2, s2 = b[i]
        if g in (I._OBJET,):
            c1, sl1 = s
            c2, sl2 = s2
            for nom in set(c1) | set(c2):
                if nom not in c1 or nom not in c2 or not _egal(c1[nom], c2[nom]):
                    ecarts.append(f"ATTR {type(o).__name__}.{nom} : {_court(c1.get(nom))} -> {_court(c2.get(nom))}")
            for nom in set(sl1) | set(sl2):
                if nom not in sl1 or nom not in sl2 or not _egal(sl1[nom], sl2[nom]):
                    ecarts.append(f"SLOT {type(o).__name__}.{nom} : {_court(sl1.get(nom))} -> {_court(sl2.get(nom))}")
        elif g in (I._LISTE, I._FILE):
            if len(s) != len(s2) or any(not _egal(x, y) for x, y in zip(s, s2)):
                ecarts.append(f"LISTE (dans {type(o).__name__}) {len(s)} -> {len(s2)} elements")
        elif g == I._DICT:
            if set(map(id, s)) != set(map(id, s2)) and set(s) != set(s2):
                ecarts.append(f"DICT {len(s)} -> {len(s2)} cles")
            else:
                for k in s:
                    if k in s2 and not _egal(s[k], s2[k]):
                        ecarts.append(f"DICT[{_court(k, 30)}] : {_court(s[k])} -> {_court(s2[k])}")
        elif g == I._ENSEMBLE:
            if s != s2:
                ecarts.append(f"ENSEMBLE {len(s)} -> {len(s2)} elements")
        elif g == I._CELLULE:
            if not _egal(s, s2):
                ecarts.append(f"CELLULE {_court(s)} -> {_court(s2)}")
    nouveaux = [type(o).__name__ for i, (g, o, s) in b.items() if i not in a and type(o).__name__ not in ("dict", "list", "set", "deque")]
    if nouveaux:
        from collections import Counter
        ecarts.append(f"FUITE : {len(nouveaux)} objet(s) CREES APRES la reference sont encore atteignables : {dict(Counter(nouveaux).most_common(6))}")
    return ecarts


def etat_exterieur(cm=None):
    from engine.lib import Random
    e = {"hasard_compteur": Random.counter, "hasard_etats": len(Random.states)}
    if cm is not None:
        r = cm.replay
        e.update({"historique": len(r.history_inputs), "pas": (r.current_step_id, r.replay_step_id), "crc": len(r.calculated_crc),
                  "undo": (cm.undo.last_step, cm.undo.next_step, cm.undo.debut_action, cm.undo.joueur_action)})
    return e


# ------------------------------------------------------------------ la sonde
def envelopper(pilote, monde, etiquette):
    """Compare l'etat RESTAURE a une reference prise AU MEME INSTANT que l'instantane du moteur (dans `PileInstantanes.prendre`, avant le
    calcul des options de la question) : comparer apres la re-pose de la question melangerait les defauts de restauration avec les objets
    transitoires que le calcul des options recree (messages, couts, contextes)."""
    from game.world import instantane as I
    from game.world.instantane import Instantane

    rng = random.Random(0xA117)  # graine de LA SONDE : independante de celle de la partie
    st = {"n_annulations": 0, "n_ecarts": 0, "rapports": [], "n_refs": 0}
    sortie = f"/tmp/sonde_annuler_{etiquette}.json"

    def ecrire():
        with open(sortie, "w") as f:
            json.dump({"annulations": st["n_annulations"], "annulations_avec_ecart": st["n_ecarts"], "rapports": st["rapports"][:40]}, f,
                      ensure_ascii=False, indent=1)

    prendre_origine = I.PileInstantanes.prendre
    restaurer_origine = I.PileInstantanes.restaurer

    def prendre(self, racines, exclus, controller_manager, locales):
        prendre_origine(self, racines, exclus, controller_manager, locales)
        refs = self.__dict__.setdefault("_sonde_refs", [])
        ref = None
        if rng.random() < PROBA:
            ref = (Instantane(racines, exclus), photo_globales(), etat_exterieur(controller_manager), racines, exclus, controller_manager)
            st["n_refs"] += 1
        refs.append(ref)
        del refs[:-self.PROFONDEUR_MAX]

    def restaurer(self, en_action):
        refs = self.__dict__.get("_sonde_refs", [])
        idx = len(self.pile) - 1 if en_action else len(self.pile) - 2
        ref = refs[idx] if 0 <= idx < len(refs) else None
        locales = restaurer_origine(self, en_action)
        del refs[idx:]
        if ref is not None:
            instantane_ref, glob, ext, racines, exclus, cm = ref
            maintenant = Instantane(racines, exclus)
            ecarts = comparer_instantanes(instantane_ref, maintenant) + ecarts_globales(glob, photo_globales())
            nouvel_ext = etat_exterieur(cm)
            for cle in ext:
                if ext[cle] != nouvel_ext.get(cle):
                    ecarts.append(f"EXTERIEUR {cle} : {ext[cle]} -> {nouvel_ext.get(cle)}")
            st["n_annulations"] += 1
            if ecarts:
                st["n_ecarts"] += 1
                st["rapports"].append({"annulation": st["n_annulations"], "ecarts": ecarts[:MAX_ECARTS_PAR_ANNULATION], "total": len(ecarts)})
                print(f"SONDE ANNULATION n°{st['n_annulations']} : {len(ecarts)} ECART(S)", flush=True)
                for e in ecarts[:MAX_ECARTS_PAR_ANNULATION]:
                    print("SONDE   ", e, flush=True)
            else:
                print(f"SONDE ANNULATION n°{st['n_annulations']} : etat identique a la reference", flush=True)
            ecrire()
        return locales

    I.PileInstantanes.prendre = prendre
    I.PileInstantanes.restaurer = restaurer

    def sonde(self, data, player_id, check):
        w = monde()
        undo = w.controller_manager.undo
        pile = undo.pile_instantanes
        if getattr(data, "event_name", "") == "WhenPlayerInTurn" and pile is not None and not w.scene.manuel_commands \
                and pile.peut_annuler(False):
            refs = pile.__dict__.get("_sonde_refs", [])
            idx = len(pile.pile) - 2
            if 0 <= idx < len(refs) and refs[idx] is not None and rng.random() < 0.7:
                undo.restauration_demandee = True
                return json.dumps({"id": "0", "targets": [], "resources": []})
        return pilote(self, data, player_id, check)

    return sonde
