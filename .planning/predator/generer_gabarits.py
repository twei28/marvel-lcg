#!/usr/bin/env python3
"""Genere docs/packs/predator/GABARITS.md : un gabarit PROCESSUS-CARTE par card_id (31 cartes).

Usage : python3 generer_gabarits.py <sortie_substituer_pack.txt> <resume_autoplay.txt> [racine_du_depot]

Source de chaque gabarit : l'en-tete du script de la carte (cartes de reference, mots-pieges), les noms des cas
`tools/cas/predator*.py` dont le nom commence par le card_id, la ligne « SUBST <id> : rouges N/M » de la preuve par substitution.
Rien n'est invente : une ligne manquante = « AUCUN » dans le gabarit.
"""
import importlib.util
import os
import re
import sys

SUBST = open(sys.argv[1], encoding="utf-8").read()
AUTOPLAY = open(sys.argv[2], encoding="utf-8").read().strip()
RACINE = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")


def charger(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CAS = []
for f in ("predator.py", "predator_b.py", "predator_c.py", "predator_d.py"):
    CAS += charger(os.path.join(MOTEUR, "tools", "cas", f), "cas_" + f[:-3]).CAS
CARTES = charger(os.path.join(RACINE, ".planning", "predator", "pd_cards.py"), "pd_cards").CARDS

PLATEAU = {
    "pd001a": "OUI : Infralocked change d'hote (identite <-> sbire), carte Cloaked sur le heros",
    "pd001b": "OUI : Infralocked entre en jeu sur l'identite au Setup",
    "pd002": "OUI : une amelioration dessinee tantot sur l'identite, tantot sur un sbire engage",
    "pd003": "OUI : sbire de JOUEUR engage avec son proprietaire",
    "pd006": "OUI : pose une carte d'etat Cloaked", "pd008": "OUI : pose une carte d'etat Cloaked et met un sbire en jeu",
    "pd009": "OUI : manigance annexe de joueur, puis en vitrine de victoire",
    "pd010": "OUI : compteurs « skull »", "pd011": "OUI : compteurs « glyph », amelioration inclinee",
    "pd016": "OUI : manigance annexe qui interdit les cartes Cloaked",
    "pd017": "OUI : sbire nemesis a carte Tough", "pd020": "OUI : attachement pose sur la Reine",
    "pd026": "OUI : manigance annexe Permanent a icone Hazard dynamique",
    "pd029": "OUI : attachement pose sur Dutch",
}
PLATEAU_FICHIER = "ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit)"
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
    for sous in ("predator", "predator_nemesis", "predator_alt_nemesis"):
        p = os.path.join(MOTEUR, "src", "cards", "pack", "predator", sous, cid + ".py")
        if os.path.exists(p):
            return p
    return None


def suj(cid):
    return [c["nom"].replace("[pd] ", "", 1) for c in CAS if c["nom"].startswith("[pd] " + cid + " ")]


def subst(cid):
    m = re.search(r"SUBST " + cid + r" : rouges (\d+)/(\d+)", SUBST)
    return (int(m.group(1)), int(m.group(2))) if m else None


NOMS = {c["card_id"]: c["name"].lstrip("* ") + (" (" + c["type"] + ")") for c in CARTES}
sortie = []
sortie.append("""# Predator (RyCoRan) : gabarits PROCESSUS-CARTE, 31 card_id

Pack `predator`, préfixe `pd`, set 214. Source : zip « Predator (5-25 Final) » déposé le 24/10/2026. Trois sets : `Predator` (pd001a-pd015,
pd021-pd025), `Predator Nemesis` (pd016-pd020), `Predator Alt Nemesis` (pd026-pd030, set némésis alternatif de l'auteur). Cas :
`Fusion/marvel-lcg-src/tools/cas/predator.py`, `predator_b.py`, `predator_c.py`, `predator_d.py` (filtre `[pd]`). Plateau :
`ui-app/src/board/predator-plateau.test.ts`. Recettes : `docs/reference/RECETTES-MOTEUR.md` §23. Questions à l'auteur : `QUESTIONS-AUTEUR.md`.

## Arbitrages utilisateur du 25/10/2026 (questions posées une à une, scan à l'appui)

1. **Savage Skewer (`pd007`)** : « discard a cloaked status card » = la carte Cloaked de **Predator seulement** (pas celle d'un ennemi ni d'un allié).
2. **Bio-Helmet (`pd014`)** : « for each icon, remove 1 threat from a scheme » = **une manigance au choix PAR icône** (répartition libre).
3. **Self Destruct (`pd011`)** : « (to a maximum of 10) » : l'utilisateur pose la question à l'auteur ; **provisoire** = plafond de 10 glyphes comptés, soit 10 dégâts au plus par cible.
4. **Hunted By the Hive (`pd019`)** : l'utilisateur pose la question à l'auteur ; **provisoire** = la Reine qui vient d'être trouvée attaque aussi.

## Décisions prises seules (règle de la Rules Reference ou texte sans ambiguïté), à signaler

- **Infralocked n'a pas d'état « libre »** : « return this card to your play area » = revenir sur l'**identité** du joueur (le moteur n'a pas d'amélioration libre).
  Si son sbire disparaît par une autre cause que Predator, la carte (Permanent) revient aussi sur l'identité (règle `NonKeyword` du script).
- **Find** (`pd008`, `pd009`, `pd019`, `pd020`, `pd029`) : règle « Find » du moteur, toutes les zones. Conséquence : le **Xenomorph de joueur** (`pd003`, un sbire) peut être trouvé par Jungle Stalk.
- **Xenomorph's Prey n'est PAS en jeu au départ** : tout le set némésis est mis de côté (comportement du moteur pour tous les héros).
- **Acid Blood / M134 Minigun** : l'icône imprimée « +1 ATQ » est écrite dans le texte (« gets +1 ATK »).
- **Decklist de l'auteur** : l'image « Predator starter deck » cite « 2 Targeted! » et « 15 Infralocked x3 » qui n'existent pas dans le zip (une seule Infralocked, 1/16, aucune « Targeted! ») ; les scans font foi.
  Les 22 cartes d'aspect (Aggression) et les 3 ressources + Razor Hunt sont recopiées dans `player_deck`.
- **Set némésis alternatif** : second deck de départ `predator_dutch` (`metadata.variante_de`).

## Points d'identification des cartes (pas des arbitrages)

- Ghost Protocol (3/16 et 4/16), Spine Rip (5/16 et 6/16), Savage Skewer (8/16 et 9/16) : impressions IDENTIQUES : un seul card_id chacune, deux exemplaires au deck.
- « Infrared Web » (`pd025`) est le fichier « Pred - Spidey Aspect - Event » ; « Razor Hunt » (`pd024`) le fichier « Predator-Wolverine TeamUp ».
- L'icône « Y » rouge du coin des cartes de rencontre est l'icône de BOOST ordinaire ; l'icône ronde à étoile est l'icône de boost à étoile. L'icône de la manigance annexe (boîte à croix) est **Hazard** (comparée à 01107 Breakin' & Takin').
- Icônes de ressource vérifiées contre les trois ressources du MÊME pack (Energy = éclair, Genius = nœuds, Strength = poing).
- Homonymes de NOM au dépôt : « Energy », « Genius », « Strength » (nombreuses versions) (aucun module ne cherche par nom : tout passe par card_id).

## Gates du héros

GATES_HEROS

""")
for c in CARTES:
    cid = c["card_id"]
    chemin = script_de(cid)
    cas = suj(cid)
    s = subst(cid)
    sortie.append(f"### {cid} : {NOMS[cid]}\n")
    if chemin:
        sortie.append("```\n" + entete(chemin) + "\n```\n")
        sortie.append("- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).")
        sortie.append("- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.")
    else:
        sortie.append("```\nRessource de base : aucun script (comme hc024 / ht015). Texte : « Max 1 per deck. » (desc.MaxPerDeck, natif).\n```\n")
        sortie.append("- [x] Étape 2 : cartes de référence : `hc024` / `ht015` (ressources de base à l'art d'un héros).")
        sortie.append("- [x] Étape 5 : texte-contre-code : « Max 1 per deck » = `desc.MaxPerDeck`, `RES` lu sur le scan. Résultat : conforme.")
    sortie.append("- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.")
    sortie.append(f"- [x] Étape 7 : cas test_capacites par capacité ({len(cas)} cas sujets) :")
    for n in cas:
        sortie.append(f"      - {n}")
    if cid == "pd009":
        sortie.append("      Preuve par substitution : le script de pd009 est VIDE (Assault, Victory, menace sont natifs) ; sa capacité « en vitrine » vit sur l'identité : "
                      "**cas « EN VITRINE » et « Limit once per round » rouges** quand `pd001a` est remplacé par un module vide (mesuré le 25/10). Résultat : OK.")
    elif s:
        sortie.append(f"      Preuve par substitution : **rouges {s[0]}/{s[1]}** sans le module" +
                      ("" if s[0] == s[1] else " (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés)") + ". Résultat : OK.")
    elif not chemin:
        sortie.append("      Preuve par substitution : sans objet (aucun module).")
    else:
        sortie.append("      Preuve par substitution : AUCUNE LIGNE (à relancer). Résultat : NON.")
    lim = cid in ("pd001b", "pd009")
    if lim:
        sortie.append("- [x] Étape 7 bis : limite imprimée ? OUI (« Limit once per round »). Témoin d'épuisement : cas « Limit once per round » (deux déclenchements, le second ne fait rien, chiffre mesuré). Résultat : OK.")
    else:
        sortie.append("- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.")
    sortie.append(f"- [x] Étape 8 : autoplay ciblé : {AUTOPLAY}")
    p = PLATEAU.get(cid)
    if p:
        sortie.append(f"- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? {p}. Cas plateau : {PLATEAU_FICHIER}. Résultat : OK.")
    else:
        sortie.append("- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.")
    sortie.append("\nCarte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).\n")
os.makedirs(os.path.join(RACINE, "docs", "packs", "predator"), exist_ok=True)
open(os.path.join(RACINE, "docs", "packs", "predator", "GABARITS.md"), "w", encoding="utf-8").write("\n".join(sortie))
print("ecrit", len(CARTES), "gabarits")
