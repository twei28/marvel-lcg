#!/usr/bin/env python3
"""Verifie la FORME d'une livraison de HEROS (20/10/2026). Python 3.8+, bibliotheque standard seulement.

    python3 verifier-livraison-heros.py <dossier livraison> [--reference <dossier reference>] [--officiel]
    python3 verifier-livraison-heros.py <dossier livraison> --moteur <racine du moteur>
    python3 verifier-livraison-heros.py --generer-reference <racine du moteur> <dossier sortie>

POURQUOI CET OUTIL
------------------
Il attrape ce qu'une IA (ou un humain) peut corriger SEUL avant de livrer un heros : une face a/b qui manque, un
deck de depart qui cite une carte absente ou la carte SIGNATURE D'UN AUTRE HEROS, une obligation qui n'est pas
adressee au bon alter ego, un set nemesis qui ne correspond pas a son fichier, un `player_deck` invente pour un
heros maison, une carte a capacite imprimee sans script, un trait ou un compteur inconnu du moteur, un texte
francais ou une biographie qui manque.

Il reutilise le controle des cartes, des scripts, des textes francais, des prefixes et du manifeste de
`verifier-livraison-campagne.py` (a cote de ce fichier) et y ajoute tout ce qui est propre a un heros.

IL NE REMPLACE PAS LE JEU. Un script qui passe ce controle peut encore ne rien faire en partie : c'est le travail
des cas de test (`tools/cas`), de `verifier_tous_les_decks.py` et d'une vraie partie. Un AVERTISSEMENT est un doute
que la livraison doit expliquer dans `QUESTIONS.md` ou `BESOINS-MOTEUR.md`.

Sortie : une ligne par probleme, `ERREUR` (bloquant, code de retour 1) ou `AVERTISSEMENT`.
"""
import argparse
import collections
import importlib.util
import io
import json
import os
import re
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))


def charger_campagne():
    chemin = os.path.join(ICI, "verifier-livraison-campagne.py")
    spec = importlib.util.spec_from_file_location("verifier_livraison_campagne", chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifier_livraison_campagne"] = mod
    spec.loader.exec_module(mod)
    return mod


VC = charger_campagne()

CLES_DECK = {"version", "name", "metadata", "hero", "hero_deck", "set_aside", "obligations", "nemesis_set",
             "player_deck", "linked_identity"}
CLES_LIEE = {"hero", "hero_deck", "set_aside", "obligations", "nemesis_set", "player_deck"}
CLES_INFO_HEROS = {"bio", "bioEn", "civil", "civilEn", "base", "baseEn", "equipes", "equipesEn", "ennemis",
                   "ennemisEn", "apparition"}
CLES_DECKBUILDING = {"aspects", "hors_aspect", "types_interdits", "types_interdits_aspect", "ressources_egales", "path"}
STATS_HERO = ("HP", "ATK", "THW", "DEF", "HS")
STATS_ALTER = ("HP", "REC", "HS")
NOTE_DECKLIST = re.compile(r"decklist|deck list|liste", re.I)


def ecrire_json_ref(dossier, nom, valeur):
    with io.open(os.path.join(dossier, nom), "w", encoding="utf-8", newline="") as f:
        json.dump(valeur, f, ensure_ascii=False, indent=1)


def generer_reference(moteur, sortie):
    """La reference de la campagne + ce qu'il faut pour un heros : les decks existants et les cartes signature."""
    VC.generer_reference(moteur, sortie)
    cartes = VC.lire_json(os.path.join(moteur, "data", "cards.json"))
    signature, noms = {}, {}
    for pack, liste in cartes.items():
        if pack == "checksum":
            continue
        for c in liste:
            cid = c.get("card_id")
            if not cid:
                continue
            noms[cid] = (c.get("name") or "").lstrip("* ").strip()
            if "Hero" in str((c.get("desc") or {}).get("Class", "")).split(";"):
                signature[cid] = c.get("set_name", "")
    decks = {}
    for f in sorted(os.listdir(os.path.join(moteur, "deck", "starter"))):
        if f.endswith(".json"):
            d = VC.lire_json(os.path.join(moteur, "deck", "starter", f))
            decks[f[:-5]] = {"hero": d.get("hero", []), "name": d.get("name", "")}
    ecrire_json_ref(sortie, "cartes-signature.json", signature)
    ecrire_json_ref(sortie, "noms-de-cartes.json", noms)
    ecrire_json_ref(sortie, "decks-existants.json", decks)
    print("reference heros : %d cartes signature, %d decks de depart" % (len(signature), len(decks)))


class LivraisonHeros(VC.Livraison):
    def __init__(self, racine, ref, rapport, officiel, extras):
        super().__init__(racine, ref, rapport, officiel)
        self.signature = extras["signature"]
        self.noms = extras["noms"]
        self.decks_existants = extras["decks"]
        self.decks = {}          # id de deck -> contenu
        self.nemesis_livres = {}
        self.marqueurs = 0

    # ---- structure : pas de carnet de campagne dans une livraison de heros
    def verifier_structure(self):
        r = self.r
        if not os.path.isdir(self.integ):
            r.erreur("livraison", "le dossier `integration/` est introuvable")
            return False
        for nom, grave in (("MANIFESTE.md", True), ("QUESTIONS.md", False), ("BESOINS-MOTEUR.md", False),
                           ("A_FAIRE_CLAUDE.md", False), ("AUTO-VERIFICATION.md", False), ("GABARITS.md", False),
                           ("images.md", False), ("CREDITS.md", False)):
            if not os.path.exists(os.path.join(self.racine, nom)):
                (r.erreur if grave else r.avert)(nom, "fichier de suivi absent de la livraison")
        besoins = os.path.join(self.racine, "BESOINS-MOTEUR.md")
        self.besoins = VC.lire(besoins) if os.path.exists(besoins) else ""
        for sous in ("scenarios", "encounter_sets", "campagnes"):
            if os.path.isdir(self.chemin("data", sous)) and self.fichiers(os.path.join("data", sous), ".json"):
                r.erreur("data/" + sous, "une livraison de HEROS ne contient ni scenario, ni set de rencontre, ni campagne "
                                         "(le set nemesis du heros vit dans `deck/starter/<id>.json`)")
        return True

    # ---- aides
    def carte(self, cid):
        return self.cartes.get(cid)

    def classe_signature(self, cid):
        """(est signature, set_name) d'une carte livree ou existante."""
        c = self.cartes.get(cid)
        if c is not None:
            return ("Hero" in str((c.get("desc") or {}).get("Class", "")).split(";"), c.get("set_name", ""))
        if cid in self.signature:
            return True, self.signature[cid]
        return False, (self.ref.ids.get(cid) or {}).get("set_name", "")

    def existe(self, cid):
        return cid in self.cartes or cid in self.ref.ids

    def nom_de(self, cid):
        c = self.cartes.get(cid)
        if c is not None:
            return (c.get("name") or "").lstrip("* ").strip()
        return self.noms.get(cid, "")

    # ---- les faces du heros
    def verifier_identites(self):
        """Une identite = une paire a/b ; une forme de plus (Ant-Man geant `c`, Moon Knight `c`-`e`) est une face de plus."""
        r = self.r
        identites = collections.OrderedDict()
        for cid, c in sorted(self.cartes.items()):
            if c.get("type") in ("Hero", "AlterEgo"):
                identites.setdefault(cid[:-1], {})[cid[-1]] = c
        if not identites:
            r.erreur("cartes", "aucune carte de type `Hero` ni `AlterEgo` : ce n'est pas un pack de heros")
            return
        self.heros_faces = {}
        for tronc, faces in identites.items():
            a, b = faces.get("a"), faces.get("b")
            if a is None or a.get("type") != "Hero":
                r.erreur("[%sa]" % tronc, "il manque la face HEROS `%sa` (type `Hero`) : elle ouvre la paire" % tronc)
            else:
                self.heros_faces[tronc + "a"] = a
            if b is None or b.get("type") != "AlterEgo":
                r.erreur("[%sb]" % tronc, "il manque la face ALTER EGO `%sb` (type `AlterEgo`) : c'est la face de depart" % tronc)
            for lettre, c in faces.items():
                loc = "[%s%s]" % (tronc, lettre)
                desc = c.get("desc") or {}
                champs = STATS_HERO if c.get("type") == "Hero" else STATS_ALTER
                for k in champs:
                    if k not in desc:
                        r.erreur(loc, "desc.%s absente (une face %s porte %s)"
                                 % (k, "heros" if c.get("type") == "Hero" else "alter ego", " ".join(champs)))
                if c.get("type") == "AlterEgo":
                    for k in ("ATK", "THW", "DEF"):
                        if k in desc:
                            r.avert(loc, "desc.%s sur un alter ego : ATK/THW/DEF sont des valeurs d'une face heros" % k)
                if not str(c.get("name", "")).startswith("* "):
                    r.avert(loc, "le nom d'une identite commence par `* ` (carte unique)")
                if c.get("set_name") != (a or c).get("set_name"):
                    r.erreur(loc, "les faces de l'identite n'ont pas le meme set_name (%r / %r)" % (c.get("set_name"), (a or c).get("set_name")))
        if len(identites) > 1:
            r.avert("cartes", "%d identites dans ce pack (%s) : seul Ironheart est ainsi ; est-ce une `linked_identity` (Cloak & Dagger) ?"
                    % (len(identites), ", ".join(identites)))

    # ---- les decks de depart
    def charger_decks(self):
        r = self.r
        base = self.chemin("deck", "starter")
        if not os.path.isdir(base):
            r.erreur("deck/starter/", "aucun deck de depart : sans lui le heros n'apparait NULLE PART dans le jeu "
                                      "(`catalog.heroes()` liste `deck/starter/*.json`)")
            return
        for f in sorted(os.listdir(base)):
            if not f.endswith(".json"):
                r.avert("deck/starter/" + f, "fichier inattendu")
                continue
            lieu = "deck/starter/" + f
            try:
                self.decks[f[:-5]] = VC.lire_json(os.path.join(base, f))
            except Exception as e:
                r.erreur(lieu, "JSON invalide : %s" % e)
        if not self.decks:
            r.erreur("deck/starter/", "aucun deck de depart : sans lui le heros n'apparait NULLE PART dans le jeu")
        nem = self.chemin("data", "nemesis")
        if os.path.isdir(nem):
            for f in sorted(os.listdir(nem)):
                if f.endswith(".json"):
                    try:
                        self.nemesis_livres[f[:-5]] = VC.lire_json(os.path.join(nem, f))
                    except Exception as e:
                        r.erreur("data/nemesis/" + f, "JSON invalide : %s" % e)

    def verifier_decks(self):
        r = self.r
        if not self.decks:
            return
        racines = [d for d, v in self.decks.items() if not (v.get("metadata") or {}).get("variante_de")]
        if not racines:
            r.erreur("deck/starter/", "aucun deck de base (tous sont des variantes)")
        for did, d in sorted(self.decks.items()):
            self.verifier_un_deck(did, d)

    def verifier_un_deck(self, did, d):
        r = self.r
        lieu = "deck/starter/%s.json" % did
        if not re.match(r"^[a-z0-9_]+$", did):
            r.erreur(lieu, "nom de fichier : minuscules, chiffres et `_` seulement (c'est l'identifiant du heros)")
        if not isinstance(d, dict):
            r.erreur(lieu, "attendu un objet")
            return
        for k in ("version", "name", "metadata", "hero", "hero_deck", "obligations", "nemesis_set", "player_deck"):
            if k not in d:
                r.erreur(lieu, "cle absente : %s" % k)
        for k in d:
            if k not in CLES_DECK:
                r.avert(lieu, "cle inconnue du format : %s" % k)
        if "set_aside" not in d:
            r.avert(lieu, "`set_aside` absent (liste, vide en pratique : le moteur ne la lit pas en partie)")
        elif d["set_aside"]:
            r.avert(lieu, "`set_aside` rempli : le moteur NE LIT PAS ce champ en vraie partie ; une carte mise de cote "
                          "se cree par `AbilityFactory.BeginGameWithSetAside` sur l'alter ego (chapitre 6)")
        if d.get("version") not in ("0.5.8", "0.5.9"):
            r.erreur(lieu, "`version` doit valoir \"0.5.8\" (ou \"0.5.9\")")
        if not isinstance(d.get("name"), str) or not d.get("name"):
            r.erreur(lieu, "`name` : le nom affiche du heros (texte non vide)")
        meta = d.get("metadata")
        if not isinstance(meta, dict):
            r.erreur(lieu, "`metadata` doit etre un objet (au minimum {\"url\": \"\"})")
            meta = {}
        elif "url" not in meta:
            r.avert(lieu, "`metadata.url` absent (la source du heros, ou \"\")")
        # deck existant ?
        if did in self.decks_existants:
            deja = self.decks_existants[did]
            if deja.get("hero") == d.get("hero"):
                self.re_livraison = True
                r.avert(lieu, "ce deck existe deja dans le jeu avec la meme identite : re-livraison d'un heros deja integre ?")
            else:
                r.erreur(lieu, "l'identifiant de deck %r EXISTE deja dans le jeu pour un autre heros" % did)
        # identite
        hero = d.get("hero")
        face_heros = None
        if not (isinstance(hero, list) and len(hero) == 1 and isinstance(hero[0], str) and re.match(r"^[0-9a-z]+(,[0-9a-z]+)+$", hero[0])):
            r.erreur(lieu, "`hero` : une liste d'UNE chaine \"<face a>,<face b>[,<forme de plus>...]\" (ex. [\"lj001a,lj001b\"])")
        else:
            a, b = hero[0].split(",")[:2]
            face_heros = a
            for plus in hero[0].split(",")[2:]:
                if not self.existe(plus):
                    r.erreur(lieu, "`hero` cite une carte inconnue : %s" % plus)
            ca, cb = self.cartes.get(a), self.cartes.get(b)
            for cid in (a, b):
                if not self.existe(cid):
                    r.erreur(lieu, "`hero` cite une carte inconnue : %s" % cid)
            if ca is not None and ca.get("type") != "Hero":
                r.erreur(lieu, "`hero` : %s doit etre de type Hero (c'est la PREMIERE face de la paire)" % a)
            if cb is not None and cb.get("type") != "AlterEgo":
                r.erreur(lieu, "`hero` : %s doit etre de type AlterEgo (c'est la SECONDE face de la paire)" % b)
        set_heros = None
        if face_heros:
            _, set_heros = self.classe_signature(face_heros)
        self.verifier_hero_deck(lieu, d, set_heros)
        self.verifier_obligations(lieu, d, hero)
        self.verifier_nemesis(lieu, d, did, set_heros, hero)
        self.verifier_player_deck(lieu, d, meta, set_heros)
        self.verifier_metadata(lieu, did, d, meta)
        if "linked_identity" in d:
            self.verifier_identite_liee(lieu, d["linked_identity"])

    def verifier_hero_deck(self, lieu, d, set_heros):
        r = self.r
        liste = d.get("hero_deck")
        if not isinstance(liste, list):
            r.erreur(lieu, "`hero_deck` doit etre une liste de card_id")
            return
        if not liste:
            r.erreur(lieu, "`hero_deck` vide : un heros a ses cartes signature (15 pour 145 des 152 decks du jeu)")
        elif len(liste) != 15 and "linked_identity" not in d:
            r.avert(lieu, "`hero_deck` compte %d cartes (15 pour 145 des 152 decks du jeu) : a justifier dans QUESTIONS.md "
                          "(deck imprime reellement different ?)" % len(liste))
        compte = collections.Counter(liste)
        for cid, n in compte.items():
            if not isinstance(cid, str) or not self.existe(cid):
                r.erreur(lieu, "hero_deck : carte inconnue %r" % (cid,))
                continue
            est_sig, set_c = self.classe_signature(cid)
            if not est_sig:
                r.avert(lieu, "hero_deck : %s (%s) n'est pas de classe `Hero` : une carte signature porte desc.Class = \"Hero\""
                        % (cid, self.nom_de(cid)))
            elif set_heros and set_c != set_heros:
                r.erreur(lieu, "hero_deck : %s (%s) est la carte SIGNATURE D'UN AUTRE HEROS (set %r, ici %r) : jamais dans ce deck"
                         % (cid, self.nom_de(cid), set_c, set_heros))
            mx = (self.cartes.get(cid) or {}).get("desc", {}).get("MaxPerDeck")
            limite = int(mx) if str(mx or "").isdigit() else 3
            if n > limite:
                r.avert(lieu, "hero_deck : %s en %d exemplaires (limite %s)" % (cid, n, limite))
        # cartes signature livrees mais absentes du deck
        if set_heros:
            dans = set(liste)
            for cid, c in self.cartes.items():
                if c.get("set_name") == set_heros and "Hero" in str((c.get("desc") or {}).get("Class", "")).split(";") \
                        and cid not in dans and not (d.get("player_deck") and cid in d["player_deck"]):
                    r.avert(lieu, "la carte signature %s (%s) est livree mais n'est dans aucun deck" % (cid, c.get("name")))

    def verifier_obligations(self, lieu, d, hero):
        r = self.r
        liste = d.get("obligations")
        if not isinstance(liste, list):
            r.erreur(lieu, "`obligations` doit etre une liste")
            return
        if len(liste) == 0:
            r.avert(lieu, "aucune obligation (148 decks sur 152 en ont UNE) : a justifier (carte non publiee ?) dans QUESTIONS.md")
        elif len(liste) > 1:
            r.avert(lieu, "%d obligations (une seule pour 148 decks sur 152)" % len(liste))
        alter = None
        if isinstance(hero, list) and hero and isinstance(hero[0], str) and "," in hero[0]:
            alter = self.nom_de(hero[0].split(",")[1])
        for cid in liste:
            if not self.existe(cid):
                r.erreur(lieu, "obligations : carte inconnue %r" % (cid,))
                continue
            c = self.cartes.get(cid)
            t = c.get("type") if c else (self.ref.ids.get(cid) or {}).get("type")
            if t != "Obligation":
                r.erreur(lieu, "obligations : %s est de type %r (attendu Obligation)" % (cid, t))
            if c is not None:
                give = (c.get("desc") or {}).get("GiveTo")
                if not give:
                    r.erreur(lieu, "obligation %s sans desc.GiveTo (le nom de l'ALTER EGO destinataire)" % cid)
                elif alter and give != alter:
                    r.avert(lieu, "obligation %s : GiveTo=%r mais l'alter ego s'appelle %r" % (cid, give, alter))

    def verifier_nemesis(self, lieu, d, did, set_heros, hero):
        r = self.r
        liste = d.get("nemesis_set")
        if not isinstance(liste, list):
            r.erreur(lieu, "`nemesis_set` doit etre une liste")
            return
        if len(liste) == 0:
            r.avert(lieu, "set nemesis vide (145 decks sur 152 en ont 5 cartes) : a justifier dans QUESTIONS.md")
        elif len(liste) != 5:
            r.avert(lieu, "set nemesis de %d cartes (5 pour 145 decks sur 152)" % len(liste))
        sets = set()
        sbires_marques = []
        noms_ok = set()
        if isinstance(hero, list) and hero and isinstance(hero[0], str):
            noms_ok = {self.nom_de(x) for x in hero[0].split(",")[:2]} | {d.get("name")}
        for cid in liste:
            if not self.existe(cid):
                r.erreur(lieu, "nemesis_set : carte inconnue %r" % (cid,))
                continue
            c = self.cartes.get(cid)
            if c is not None:
                sets.add(c.get("set_name"))
                if c.get("type") == "Minion" and (c.get("desc") or {}).get("Nemesis"):
                    sbires_marques.append(c)
                if c.get("type") in ("Hero", "AlterEgo", "Ally", "Event", "Upgrade", "Support", "Resource"):
                    r.erreur(lieu, "nemesis_set : %s est une carte JOUEUR (%s) : un set nemesis est fait de cartes de rencontre"
                             % (cid, c.get("type")))
        if set_heros and sets and sets != {set_heros + " Nemesis"}:
            r.avert(lieu, "set_name des cartes nemesis %s au lieu de %r (un set emprunte a un autre heros est possible, mais "
                          "a justifier)" % (sorted(str(s) for s in sets), set_heros + " Nemesis"))
        if liste and not sbires_marques and sets:
            r.avert(lieu, "aucun sbire de ce set n'est marque desc.Nemesis=\"<heros>\" : les cartes qui cherchent « le sbire "
                          "nemesis » ne le trouveront pas")
        for c in sbires_marques:
            if noms_ok and c["desc"]["Nemesis"] not in noms_ok:
                r.avert(lieu, "sbire nemesis %s : desc.Nemesis=%r n'est ni le nom du heros, ni celui de l'alter ego, ni deck.name (%s)"
                        % (c["card_id"], c["desc"]["Nemesis"], ", ".join(sorted(str(x) for x in noms_ok))))
        # fichier data/nemesis/<id>_nemesis.json facultatif : doit etre coherent
        f = self.nemesis_livres.get(did + "_nemesis")
        if f is not None:
            if f.get("encounters") != liste:
                r.erreur("data/nemesis/%s_nemesis.json" % did, "`encounters` differe de `nemesis_set` du deck de depart")
            for k in ("version", "name", "encounters"):
                if k not in f:
                    r.erreur("data/nemesis/%s_nemesis.json" % did, "cle absente : %s" % k)
            if f.get("version") not in ("0.5.8", "0.5.9"):
                r.erreur("data/nemesis/%s_nemesis.json" % did, "`version` doit valoir \"0.5.8\" (ou \"0.5.9\")")

    def verifier_player_deck(self, lieu, d, meta, set_heros):
        r = self.r
        liste = d.get("player_deck")
        if not isinstance(liste, list):
            r.erreur(lieu, "`player_deck` doit etre une liste")
            return
        if not liste:
            if self.officiel:
                r.avert(lieu, "heros officiel avec `player_deck` vide : la boite imprime un deck de depart ; s'il n'est pas "
                              "publie, dis-le dans metadata.deck_note")
            return
        notes = " ".join(str(meta.get(k, "")) for k in ("note", "deck_note", "decklist_source"))
        if not self.officiel and not NOTE_DECKLIST.search(notes):
            r.erreur(lieu, "`player_deck` NON VIDE pour un heros maison sans note qui cite la decklist de l'AUTEUR "
                           "(metadata.note : « Decklist officielle du scan ... ») : un deck d'aspect INVENTE est interdit, "
                           "`player_deck` reste vide (consigne du 06/09/2026)")
        if len(liste) < 24:
            r.avert(lieu, "player_deck de %d cartes (24 a 27 pour 99 decks sur 100 non vides)" % len(liste))
        for cid in set(liste):
            if not self.existe(cid):
                r.erreur(lieu, "player_deck : carte inconnue %r" % (cid,))
                continue
            est_sig, set_c = self.classe_signature(cid)
            if est_sig and set_heros and set_c != set_heros:
                r.erreur(lieu, "player_deck : %s (%s) est la carte SIGNATURE D'UN AUTRE HEROS (set %r) : le moteur ne valide pas "
                               "les decks de depart, c'est a toi de l'eviter" % (cid, self.nom_de(cid), set_c))

    def verifier_metadata(self, lieu, did, d, meta):
        r = self.r
        auteur = meta.get("author") or meta.get("auteur")
        cartes_h = [c for c in self.cartes.values() if c.get("type") == "Hero"]
        if not self.officiel and not auteur:
            r.avert(lieu, "metadata.author (ou auteur) absent : le nom du createur du heros")
        elif not self.officiel and auteur and cartes_h and not any(auteur == c.get("custom") for c in cartes_h):
            r.avert(lieu, "metadata.author %r differe de la cle `custom` des cartes heros" % auteur)
        variante_de = meta.get("variante_de")
        if variante_de:
            if variante_de not in self.decks and variante_de not in self.decks_existants:
                r.erreur(lieu, "variante_de : le deck de base %r n'existe pas" % variante_de)
            if not meta.get("variante_nom"):
                r.erreur(lieu, "une variante porte `metadata.variante_nom` (le libelle dans la modale du heros)")
        elif any((v.get("metadata") or {}).get("variante_de") == did for v in self.decks.values()) and not meta.get("variante_nom"):
            r.erreur(lieu, "ce deck a une variante : lui aussi porte `metadata.variante_nom`")
        for alt in meta.get("hero_alts", []) or []:
            if not isinstance(alt, dict) or "hero" not in alt or "name" not in alt:
                r.erreur(lieu, "hero_alts : chaque entree est {\"name\", \"hero\": [\"<a>,<b>\"], \"url\"}")
                continue
            for part in str(alt["hero"][0]).split(","):
                if not self.existe(part):
                    r.erreur(lieu, "hero_alts : carte inconnue %s" % part)
        db = meta.get("deckbuilding")
        if db is not None:
            if not isinstance(db, dict):
                r.erreur(lieu, "metadata.deckbuilding doit etre un objet")
            else:
                for k in db:
                    if k not in CLES_DECKBUILDING:
                        r.erreur(lieu, "metadata.deckbuilding : cle inconnue %r (connues : %s)" % (k, ", ".join(sorted(CLES_DECKBUILDING))))
                if "hors_aspect" in db and (not isinstance(db["hors_aspect"], dict) or "max" not in db["hors_aspect"]):
                    r.erreur(lieu, "deckbuilding.hors_aspect : {\"max\": n, \"traits\": [...], \"types\": [...], \"label\": \"...\"}")
                if "aspects" in db and (not isinstance(db["aspects"], dict) or not {"min", "max"} <= set(db["aspects"])):
                    r.erreur(lieu, "deckbuilding.aspects : {\"min\": n, \"max\": n, \"label\": \"...\"}")
            if not meta.get("deckbuilding_note"):
                r.avert(lieu, "metadata.deckbuilding sans `deckbuilding_note` (qui dit pourquoi, avec le texte imprime)")

    def verifier_identite_liee(self, lieu, lie):
        r = self.r
        if not isinstance(lie, dict):
            r.erreur(lieu, "linked_identity doit etre un objet")
            return
        for k in CLES_LIEE:
            if k not in lie:
                r.erreur(lieu, "linked_identity : cle absente %s" % k)
        for cid in list(lie.get("hero_deck", [])) + list(lie.get("player_deck", [])):
            if not self.existe(cid):
                r.erreur(lieu, "linked_identity : carte inconnue %r" % (cid,))

    # ---- sets_info : la liste `heroes`
    def verifier_sets_info_heros(self):
        r = self.r
        for cle, v in self.sets_info.items():
            if v.get("scenarios"):
                r.erreur("sets_info", "%r : `scenarios` doit etre [] pour un pack de heros" % cle)
            if v.get("encounters"):
                r.erreur("sets_info", "%r : `encounters` doit etre [] pour un pack de heros" % cle)
            heros = v.get("heroes") or []
            if not heros:
                r.erreur("sets_info", "%r : `heroes` vide : le heros n'apparaitrait dans aucune extension" % cle)
            for h in heros:
                if h not in self.decks and h not in self.decks_existants:
                    r.erreur("sets_info", "%r : heroes cite %r, qui n'a pas de deck de depart" % (cle, h))
            if not self.officiel and not re.search(r"Custom", cle):
                r.avert("sets_info", "%r : la cle d'une extension fan-made est « N. Custom (<Nom>) »" % cle)
        listes = {h for v in self.sets_info.values() for h in v.get("heroes", [])}
        for did, d in self.decks.items():
            if (d.get("metadata") or {}).get("variante_de"):
                continue
            if listes and did not in listes:
                r.avert("sets_info", "le deck %r n'est dans la liste `heroes` d'aucune extension livree" % did)

    # ---- chaque capacite imprimee a un script
    def verifier_scripts_manquants(self):
        r = self.r
        presents = set()
        for chemin in self.fichiers("src", ".py"):
            nom = os.path.basename(chemin)
            if re.match(r"^[0-9a-z]+\.py$", nom) and nom != "__init__.py":
                presents.add(nom[:-3])
        for cid, c in sorted(self.cartes.items()):
            if "full_link" in c or "ability_link" in c or cid in presents:
                continue
            txt = c.get("text") if isinstance(c.get("text"), str) else ""
            if any(m in txt for m in VC.MOTS_CAPACITE):
                r.erreur("src/", "la carte %s (%s) imprime une capacite (« %s ») mais n'a AUCUN script : sans lui elle ne fait "
                                 "rien, sans erreur" % (cid, c.get("name"), re.sub(r"\s+", " ", txt)[:50]))

    # ---- biographie et replique
    def verifier_biographie(self):
        r = self.r
        chemin = self.chemin("public", "js", "prepare", "heros-info.fragment.js")
        faces = sorted(self.heros_faces) if hasattr(self, "heros_faces") else []
        if not os.path.exists(chemin):
            (r.avert if self.officiel else r.erreur)("public/js/prepare/", "pas de biographie (`heros-info.fragment.js`) : le panneau "
                                                     "du heros dans le lanceur reste vide")
            return
        texte = VC.lire(chemin)
        blocs = re.findall(r'^\s*"([0-9a-z]+)":\s*\{(.*?)^\s*\},?\s*$', texte, re.M | re.S)
        if not blocs:
            r.erreur("heros-info.fragment.js", "aucune entree `\"<card_id de la face heros>\": { ... }` reconnue")
            return
        vus = set()
        for cid, corps in blocs:
            vus.add(cid)
            if faces and cid not in faces:
                r.erreur("heros-info.fragment.js", "%s : la biographie s'indexe par le card_id de la FACE HEROS, jamais par le nom "
                                                   "(faces livrees : %s)" % (cid, ", ".join(faces)))
            cles = set(re.findall(r"^\s{4,}([A-Za-z]+):", corps, re.M))
            for k in ("bio", "bioEn"):
                if k not in cles:
                    r.erreur("heros-info.fragment.js", "%s : `%s` absent (obligatoire)" % (cid, k))
            for k in sorted(cles - CLES_INFO_HEROS):
                r.avert("heros-info.fragment.js", "%s : cle inconnue %r" % (cid, k))
            m = re.search(r'bio:\s*"((?:[^"\\]|\\.)*)"', corps)
            if m and len(m.group(1)) > 900:
                r.avert("heros-info.fragment.js", "%s : bio de %d caracteres (3 a 4 phrases : panneau etroit)" % (cid, len(m.group(1))))
            if re.search(r"\b(Action|Response|Interrupt|Forced)\b", corps):
                r.avert("heros-info.fragment.js", "%s : la biographie decrit le PERSONNAGE, jamais sa mecanique de jeu" % cid)
        for cid in faces:
            if cid not in vus:
                r.erreur("heros-info.fragment.js", "pas de biographie pour la face heros %s" % cid)

    def verifier_repliques(self):
        chemin = self.chemin("public", "js", "prepare", "repliques-heros.fragment.js")
        if not os.path.exists(chemin):
            self.r.avert("public/js/prepare/", "pas de replique de recrutement (`repliques-heros.fragment.js`) : le heros retombe sur "
                                               "« BAM ! » (facultatif, mais a proposer a l'utilisateur)")
            return
        for i, ligne in enumerate(VC.lire(chemin).split("\n"), 1):
            if not ligne.strip() or ligne.strip().startswith("//"):
                continue
            m = re.match(r'^\s*([a-z0-9_]+):\s*\[(.*)\],?\s*$', ligne)
            if not m:
                self.r.erreur("repliques-heros.fragment.js:%d" % i, "attendu : `    <id du deck>: [\"replique\", ...],`")
                continue
            if m.group(1) not in self.decks:
                self.r.erreur("repliques-heros.fragment.js:%d" % i, "%r n'est pas l'identifiant d'un deck livre (la replique s'indexe "
                                                                    "par id de DECK, jamais par nom)" % m.group(1))
            if not re.search(r'"', m.group(2)):
                self.r.erreur("repliques-heros.fragment.js:%d" % i, "aucune replique entre guillemets")

    def verifier_decks_de_test(self):
        chemin = self.chemin("tools", "decks-de-test.fragment.json")
        if not os.path.exists(chemin):
            return
        try:
            d = VC.lire_json(chemin)
        except Exception as e:
            self.r.erreur("tools/decks-de-test.fragment.json", "JSON invalide : %s" % e)
            return
        for face, liste in (d.get("decks") or {}).items():
            if face not in self.cartes:
                self.r.erreur("tools/decks-de-test.fragment.json", "%s n'est pas une face heros livree" % face)
            for cid in liste:
                if not self.existe(cid):
                    self.r.erreur("tools/decks-de-test.fragment.json", "carte inconnue %r" % (cid,))

    def verifier_cas_heros(self):
        if not self.fichiers(os.path.join("tools", "cas"), ".py"):
            self.r.avert("tools/cas/", "aucun cas de test de capacite (`tools/cas/<heros>.py`) : les capacites ne seront prouvees "
                                       "par aucun cas ; a dire dans AUTO-VERIFICATION.md")

    def tout(self):
        if not self.verifier_structure():
            return
        self.verifier_prefixes()
        self.verifier_cartes()
        self.verifier_faces()
        self.verifier_identites()
        self.charger_decks()
        self.verifier_decks()
        self.verifier_sets_info()
        self.verifier_sets_info_heros()
        self.verifier_scripts()
        self.verifier_scripts_manquants()
        self.verifier_textes_fr()
        self.verifier_biographie()
        self.verifier_repliques()
        self.verifier_decks_de_test()
        self.verifier_images()
        self.verifier_cas()
        self.verifier_cas_heros()
        self.verifier_manifeste()
        self.replier_traits()

    def replier_traits(self):
        """Un trait inconnu revient sur chaque carte qui le porte : une seule ligne par trait, avec la liste des cartes."""
        motif = re.compile(r"^AVERTISSEMENT  (.*)\[([^\]]+)\] : trait ([\"'].+?[\"']) absent de la liste typee")
        par_trait, gardees = collections.OrderedDict(), []
        for ligne in self.r.lignes:
            m = motif.match(ligne)
            if m:
                par_trait.setdefault(m.group(3), []).append(m.group(2))
                self.r.avertissements -= 1
            else:
                gardees.append(ligne)
        for trait, ids in par_trait.items():
            gardees.append("AVERTISSEMENT  traits : %s absent de la liste typee CardFace.TRAITS (aucun controle a l'execution) : a "
                           "signaler dans BESOINS-MOTEUR.md, porte par %s" % (trait, ", ".join(ids)))
            self.r.avertissements += 1
        self.r.lignes = gardees


def charger_extras(dossier):
    def charge(nom):
        chemin = os.path.join(dossier, nom)
        return VC.lire_json(chemin) if os.path.exists(chemin) else {}
    return {"signature": charge("cartes-signature.json"), "noms": charge("noms-de-cartes.json"),
            "decks": charge("decks-existants.json")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("livraison", nargs="?")
    ap.add_argument("--reference")
    ap.add_argument("--moteur")
    ap.add_argument("--officiel", action="store_true", help="heros officiel : ni prefixe, ni custom")
    ap.add_argument("--generer-reference", nargs=2, metavar=("MOTEUR", "SORTIE"))
    args = ap.parse_args()
    if args.generer_reference:
        os.makedirs(args.generer_reference[1], exist_ok=True)
        generer_reference(*args.generer_reference)
        return 0
    if not args.livraison:
        ap.error("dossier de livraison requis")
    ref_dir = args.reference or os.path.join(ICI, "reference")
    if args.moteur:
        ref_dir = tempfile.mkdtemp(prefix="reference-heros-")
        generer_reference(args.moteur, ref_dir)
    ref = VC.Reference(ref_dir)
    if not ref.chargee:
        print("ATTENTION : aucune reference trouvee dans %s : les controles contre le jeu existant sont desactives." % ref_dir)
    rapport = VC.Rapport()
    liv = LivraisonHeros(os.path.abspath(args.livraison), ref, rapport, args.officiel, charger_extras(ref_dir))
    liv.tout()
    for ligne in rapport.lignes:
        print(ligne)
    print()
    print("%d ERREUR(S), %d AVERTISSEMENT(S)" % (rapport.erreurs, rapport.avertissements))
    return 1 if rapport.erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
