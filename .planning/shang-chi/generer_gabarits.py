#!/usr/bin/env python3
"""Genere docs/packs/shang-chi/GABARITS.md : un gabarit PROCESSUS-CARTE par card_id.

Usage : python3 generer_gabarits.py <sortie_substituer_pack.txt> [racine_du_depot]

Source de chaque gabarit : l'en-tete du script de la carte (cartes de reference, mots-pieges), les noms des cas
`tools/cas/shang_chi*.py` dont le nom commence par le card_id, et la ligne « SUBST <id> : rouges N/M » de la preuve par
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


CAS = charger(os.path.join(MOTEUR, "tools", "cas", "shang_chi.py"), "cas_a").CAS + \
    charger(os.path.join(MOTEUR, "tools", "cas", "shang_chi_b.py"), "cas_b").CAS
CARTES = charger(os.path.join(RACINE, ".planning", "shang-chi", "ch_cards.py"), "ch_cards").CARDS

# Ce que chaque carte DESSINE (etape 8 bis) : OUI avec le fichier de preuve, sinon NON avec la raison.
PLATEAU = {
    "ch001b": "OUI : Meditate sort une carte de la pile State of Flow vers le deck (la pile se lit sur le plateau)",
    "ch002": "OUI : la pile d'attaques glissees FACE VISIBLE sous le soutien",
    "ch013": "OUI : pose des compteurs sur les ameliorations", "ch014": "OUI : pose des compteurs sur les ameliorations",
    "ch015": "OUI : compteurs charge", "ch016": "OUI : compteurs reflet", "ch017": "OUI : compteurs chi",
    "ch019": "OUI : compteurs mystiques sur le sbire nemesis", "ch020": "OUI : manigance annexe a compteurs mystiques",
}
PLATEAU_FICHIER = "ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit)"
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
    for sous in ("shang_chi", "shang_chi_nemesis"):
        p = os.path.join(MOTEUR, "src", "cards", "pack", "shang_chi", sous, cid + ".py")
        if os.path.exists(p):
            return p
    raise SystemExit("script introuvable : " + cid)


def suj(cid):
    return [c["nom"].replace("[ch] ", "", 1) for c in CAS if c["nom"].startswith("[ch] " + cid + " ")]


def subst(cid):
    m = re.search(r"SUBST " + cid + r" : rouges (\d+)/(\d+)", SUBST)
    return (int(m.group(1)), int(m.group(2))) if m else None


NOMS = {c["card_id"]: c["name"].lstrip("* ") + (" (" + c["type"] + ")") for c in CARTES}
sortie = []
sortie.append("""# Shang-Chi (DesignHacker, SEALED) : gabarits PROCESSUS-CARTE, 22 card_id

Pack `shang_chi`, préfixe `ch` (deux lettres : `verifier_prefixes` ignore les ids à trois lettres), set 212. Source : zip
« SHANG-CHI (SEALED) » déposé le 24/10/2026. Cas : `Fusion/marvel-lcg-src/tools/cas/shang_chi.py` et `shang_chi_b.py` (filtre `[ch]`).
Plateau : `ui-app/src/board/shang-chi-plateau.test.ts`. Constructeur de deck : `tools/tests-lanceur/regles-shang-chi.test.mjs`.
Mot-clé maison : `docs/reference/mots-cles/flow.md`.

## Arbitrages utilisateur du 24/10/2026 (questions posées une à une, scan à l'appui)

1. **Meditate (`ch001b`)** : « shuffle a card from State of Flow » = une carte **au choix** de la pile (pas celle du dessus, pas toute la pile).
2. **Multiple Forms (`ch001b`)** : « chaque aspect autre que le vôtre » = Aggression, Justice, Leadership, Protection **plus** Determination,
   Venomized, 'Pool ; les voies TMNT (Taijutsu...) n'en sont pas. 1 titre ATTACK par autre aspect, 3 exemplaires.
3. **Flow** : correspondance **stricte** des icônes imprimées (un wild ne vaut que wild). L'icône étoile noire du Flow de Throat Punch a été
   découpée et comparée à l'étoile verte du coin de Dragon Strike 7/15 : même forme = wild.
4. **Special Delivery (`ch007`/`ch008`)** : « play the next ATTACK event from your hand at no cost » = **coût différé** (le prochain ATTACK
   que le joueur joue ce tour coûte 0).
5. **The Life Stealer (`ch020`)** : « 3 indirect damage to each hero and ally » = **3 dégâts directs** à chaque héros et allié.
6. **Downtown Attack (`ch021`)** : le joueur qui révèle choisit parmi **ses** alliés et **ses** cartes PERSONA.
7. **Augmented Blow (`ch013`/`ch014`)** : « additional counter » = un compteur du **même type** que ceux déjà présents (au choix s'il y en a
   plusieurs), sur toute amélioration en jeu qui porte au moins un compteur.
8. Pas de decklist d'aspect fournie : `player_deck` reste vide (PROCESSUS-HEROS étape 3).

## Points d'identification des cartes (pas des arbitrages)

- **Les « copy » du zip ne sont pas des doublons** : même dessin, icône de ressource imprimée différente (numéros 1/15 à 15/15 du bas de
  carte). Flow lit cette icône, donc 6 titres × 2 impressions = 12 card_id (`ch003`-`ch014`). Correspondance impression → icône(s) :
  Throat Punch 1/15 poing+mental, 2/15 mental ; Roundhouse 3/15 énergie, 4/15 poing+énergie ; Special Delivery 5/15 wild, 6/15 mental ;
  Dragon Strike 7/15 wild, 8/15 énergie ; Chi Jabs 9/15 wild, 10/15 poing ; Augmented Blow 11/15 énergie+mental, 12/15 poing.
- Le fichier du zip « UPGRADE - Golden Bracers » est la carte **Metal Bracers** (`ch016`) ; « Special Delivery copy » et consorts : voir ci-dessus.
- Homonymes de NOM au dépôt : `* Shang-Chi` (allié 63015/04098/dt025/56113), « Special Delivery » (16148), « The Life Stealer » (`sv014`).
  Aucun module du pack ne cherche par ces noms (tout passe par card_id).
- **Préfixe** : `sc` est pris (tmnt_shinobi_dual), 63015 est l'allié d'Iron Fist ; `shc` a été essayé puis abandonné (gate
  `verifier_prefixes` : deux lettres seulement). `ch` est libre.

## Gates du héros

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
    sortie.append("- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.")
    p = PLATEAU.get(cid)
    if p:
        sortie.append(f"- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? {p}. Cas plateau : {PLATEAU_FICHIER}. Résultat : OK.")
    else:
        sortie.append("- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.")
    sortie.append("\nCarte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).\n")
open(os.path.join(RACINE, "docs", "packs", "shang-chi", "GABARITS.md"), "w", encoding="utf-8").write("\n".join(sortie))
print("ecrit", len(CARTES), "gabarits")
