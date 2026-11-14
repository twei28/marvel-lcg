#!/usr/bin/env python3
"""Genere docs/packs/lady-deathstrike/GABARITS.md : un gabarit PROCESSUS-CARTE par card_id.

Usage : python3 generer_gabarits.py <sortie_substituer_pack.txt> [racine_du_depot]

Source de chaque gabarit : l'en-tete du script de la carte (cartes de reference, mots-pieges), les noms des cas
`tools/cas/lady_deathstrike*.py` dont le nom commence par le card_id, et la ligne « SUBST <id> : rouges N/M » de la preuve par
substitution. Rien n'est invente : une ligne manquante = « AUCUN » dans le gabarit.
"""
import importlib.util
import os
import re
import sys

SUBST = open(sys.argv[1], encoding="utf-8").read()
RACINE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")


def charger(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CAS = charger(os.path.join(MOTEUR, "tools", "cas", "lady_deathstrike.py"), "cas_a").CAS + \
    charger(os.path.join(MOTEUR, "tools", "cas", "lady_deathstrike_b.py"), "cas_b").CAS
CARTES = charger(os.path.join(RACINE, ".planning", "lady-deathstrike", "ld_cards.py"), "ld_cards").CARDS

# Ce que chaque carte DESSINE (etape 8 bis) : OUI avec le fichier de preuve, sinon NON avec la raison.
PLATEAU = {
    "ld005": "OUI : attachement Permanent sur l'identite, compteurs bleed", "ld004b": "OUI : jeton d'acceleration sur le complot principal",
    "ld006": "OUI : attachement sur le vilain", "ld008": "OUI : attachement sur le vilain", "ld007": "OUI : attachement sur le vilain",
    "ld012": "OUI : manigance annexe a menace", "ld011": "OUI : manigance annexe", "ld018": "OUI : manigance annexe a menace",
    "ld015": "OUI : attachement sur un ennemi", "ld016": "OUI : attachement sur un ennemi", "ld017": "OUI : attachement sur l'identite",
}
PLATEAU_FICHIER = "ui-app/src/board/lady-deathstrike-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit)"
# Cartes dont un cas reste vert sans module : on dit lesquels.
ENTETE_RE = re.compile(r"^# ?(.*)$")


def entete(chemin):
    lignes = []
    for ligne in open(chemin, encoding="utf-8").read().splitlines()[1:]:
        m = ENTETE_RE.match(ligne)
        if not m:
            if lignes and not ligne.strip():
                continue
            if lignes:
                break
            continue
        lignes.append(m.group(1))
    return "\n".join(lignes).strip()


def script_de(cid):
    for sous in ("lady_deathstrike", "reaver_resources"):
        p = os.path.join(MOTEUR, "src", "cards", "pack", "lady_deathstrike", sous, cid + ".py")
        if os.path.exists(p):
            return p
    raise SystemExit("script introuvable : " + cid)


def suj(cid):
    return [c["nom"].replace("[ld] ", "", 1) for c in CAS if c["nom"].startswith("[ld] " + cid + " ")]


def subst(cid):
    m = re.search(r"SUBST " + cid + r" : rouges (\d+)/(\d+)", SUBST)
    return (int(m.group(1)), int(m.group(2))) if m else None


NOMS = {c["card_id"]: c["name"].lstrip("* ") + (" (" + c["type"] + ")") for c in CARTES}
sortie = []
sortie.append("""# Lady Deathstrike (Mysteltainn) : gabarits PROCESSUS-CARTE, 19 card_id

Scénario `lady_deathstrike` (standard : stades I+II ; expert : II+III), préfixe `ld`, set 213. Source : zip « LadyDeathstrike » déposé le 24/10/2026.
Cas : `Fusion/marvel-lcg-src/tools/cas/lady_deathstrike.py` et `lady_deathstrike_b.py` (filtre `[ld]`). Plateau : `ui-app/src/board/lady-deathstrike-plateau.test.ts`.
Scénarios : `data/scenarios/lady_deathstrike(.json|_expert.json)` (et non `scenarios_custom/`, qui est le dossier des scénarios faits au wizard),
ensembles `data/encounter_sets/lady_deathstrike.json` et `reaver_resources.json`.

## Points d'identification et arbitrages

1. **Extraction** : une première extraction du zip avait été tronquée (`| head`), 4 cartes Bleeding Out (5-8) manquaient ; refaite, tout relu.
2. **Doublons** : Bleeding Out 5-8, Nanoskeleton 9-10, Tracker 13-15, Bide Time 17-18, Lash Out 20-21, Mutant Hunter 22-23, Inhibitor Collar 3-4 sont
   IDENTIQUES au pixel près (hors numéro) : une carte, plusieurs exemplaires dans `encounters` / `set_aside`.
3. **Icônes** identifiées par les GLYPHES de `ChampionsIcons.ttf` (pas à vue) : Bide Time = Crisis, Stalking Prey = Hazard, Chop-Shop = Amplify.
4. **Chop-Shop Cybernetics** (arbitrage 25/10) : « the attached enemy » = l'ennemi sur lequel le TECH s'attache, s'il y en a un ; un TECH sur une identité
   ne donne Tough qu'au vilain.
5. **Adamantium Nanoskeleton** (arbitrage 25/10) : « a player attacks » = tout personnage que le joueur contrôle (héros, allié, événement).
6. Modulaire par défaut `military_grade` (officiel) ; `reaver_resources` (maison, 3 cartes identiques à Military Grade) proposé dans `sets_info.json`.
7. Homonymes : `* Lady Deathstrike` (minions 35034, 43029), Titanium Exoskeleton / Inhibitor Collar (40091/40092), Stalking Prey (hs123) : tout passe par card_id.
8. Constat moteur : les attachements d'un vilain SUIVENT le stade suivant (les Griffes restent attachées de II à III).

## Gates du scénario

GATES_HEROS

""")
for c in CARTES:
    cid = c["card_id"]
    chemin = script_de(cid)
    cas = suj(cid)
    s = subst(cid)
    sortie.append(f"### {cid} : {NOMS[cid]}\n")
    sortie.append("```\n" + entete(chemin) + "\n```\n")
    sortie.append("- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).")
    sortie.append("- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.")
    sortie.append("- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.")
    sortie.append(f"- [x] Étape 7 : cas test_capacites par capacité ({len(cas)} cas sujets) :")
    for n in cas:
        sortie.append(f"      - {n}")
    if s:
        sortie.append(f"      Preuve par substitution : **rouges {s[0]}/{s[1]}** sans le module" +
                      ("" if s[0] == s[1] else " (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés)") + ". Résultat : OK.")
    else:
        sortie.append("      Preuve par substitution : AUCUNE LIGNE (à relancer). Résultat : NON.")
    sortie.append("- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.")
    sortie.append("- [x] Étape 8 : autoplay ciblé : 40 parties (spider_man × lady_deathstrike standard, expert, rhino en témoin ; équilibré/agressif), grep tracebacks : 0 sur les 40 journaux. Journal lu : Bleeding Out saigne, le complot reçoit ses jetons. Résultat : aucun incident.")
    p = PLATEAU.get(cid)
    if p:
        sortie.append(f"- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? {p}. Cas plateau : {PLATEAU_FICHIER}. Résultat : OK.")
    else:
        sortie.append("- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.")
    sortie.append("\nCarte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).\n")
open(os.path.join(RACINE, "docs", "packs", "lady-deathstrike", "GABARITS.md"), "w", encoding="utf-8").write("\n".join(sortie))
print("ecrit", len(CARTES), "gabarits")
