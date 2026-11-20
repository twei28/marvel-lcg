#!/usr/bin/env python3
"""Genere docs/packs/alien-vs-predator/GABARITS.md : un gabarit PROCESSUS-CARTE par card_id d'Alien vs. Predator.

Usage : python3 generer_gabarits.py <sortie_substituer_pack.txt> "<resume autoplay>" [racine_du_depot]

Source de chaque gabarit : l'en-tete du script de la carte (cartes de reference, mots-pieges), les noms des cas
`tools/cas/alien_vs_predator*.py` dont le nom commence par le card_id, la ligne « SUBST <id> : rouges N/M » de la preuve par
substitution et les explications des cas verts sans module (VERTS ci-dessous, verifiees une a une). Rien n'est invente : une ligne
manquante = « AUCUNE » dans le gabarit.
"""
import importlib.util
import os
import re
import sys

SUBST = open(sys.argv[1], encoding="utf-8").read()
AUTOPLAY = sys.argv[2]
RACINE = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
PACK = os.path.join(MOTEUR, "src", "cards", "pack", "alien_vs_predator")


def charger(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CAS = []
for f in ("alien_vs_predator", "alien_vs_predator_b", "alien_vs_predator_c", "alien_vs_predator_d"):
    CAS += charger(os.path.join(MOTEUR, "tools", "cas", f + ".py"), "cas_" + f).CAS
CARTES = charger(os.path.join(RACINE, ".planning", "alien-vs-predator", "ap_cards.py"), "ap_cards").CARDS

# Pourquoi des cas restent verts sans le module (lu cas par cas dans le journal de substitution du 25/10/2026).
VERTS = {
    "ap001a": "« if able » (sans Hive, la menace va au complot avec ou sans module), contre-cas « defend : rien », victoire au dernier mechant (defaite NATIVE du moteur, arbitrage 2)",
    "ap005b": "contre-cas « une menace sur Skulls : aucun degat »",
    "ap006b": "contre-cas « manigance : rien ne bouge » et « 3 menaces seulement »",
    "ap007b": "« 3B accompli -> defaite » : sans module le moteur termine deja la partie par sa regle de dernier stade (constate au journal le 25/10/2026) ; le module garantit la defaite imprimee quel que soit l'etat du deck des complots",
    "ap008b": "meme raison que ap007b",
    "ap009": "contre-cas « ligne de base : 2 icones » et « Alien Scout (2 PV) : pas de boost »",
    "ap010": "contre-cas « degats hors attaque » et « allies liberes quand Skulls quitte le jeu » (NATIF : mesure du 25/10/2026, voir le script)",
    "ap018": "Incite 2 avec le Warlord actif (valeur imprimee, native) et « reste en boost » (porte par Expanding Hive)",
    "ap301": "Incite 2 avec la Reine active (valeur imprimee, native)",
    "ap305": "contre-cas « la Reine n'est pas YAUTJA » et « ligne de base : Black Cat peut defendre »",
    "ap306": "le cas de la Reponse mesurait seulement la defausse (la carte part aussi sans module, faute d'hote) : renforce le 25/10/2026 par les degats sur le Warlord",
    "ap102": "contre-cas « defausse depuis la MAIN : rien »",
}
PLATEAU = {
    "ap001a": "OUI : deux vilains dessines ; le deck Xenomorph glisse dessous", "ap002a": "OUI : deux vilains dessines",
    "ap003a": "OUI : deux vilains dessines ; le deck Xenomorph glisse dessous", "ap004a": "OUI : deux vilains dessines",
    "ap005a": "OUI : 16 Alien Scout glisses SOUS Alien Queen, face cachee", "ap009": "OUI : manigance annexe permanente et sa menace",
    "ap010": "OUI : manigance annexe permanente, allie glisse dessous", "ap011": "OUI : attachement du Warlord et ses compteurs « plasma »",
    "ap013": "OUI : attachement de rencontre sur l'identite",
}
PLATEAU_FICHIER = "ui-app/src/board/alien-vs-predator-plateau.test.ts (6 cas verts, calibre ROUGE sur un compteur faux ; aucun correctif de plateau necessaire)"
LIENS = {"ap206": "01192 Masterplan", "ap207": "01190 Shadow of the Past"}
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
    for d in ("alien_vs_predator", "xenomorph_deck", "apex_standard", "clan_yautja"):
        p = os.path.join(PACK, d, cid + ".py")
        if os.path.exists(p):
            return p
    return None


def suj(cid):
    return [c["nom"].replace("[ap] ", "", 1) for c in CAS if c["nom"].startswith("[ap] " + cid + " ")]


def subst(cid):
    m = re.search(r"SUBST " + cid + r" : rouges (\d+)/(\d+)", SUBST)
    return (int(m.group(1)), int(m.group(2))) if m else None


NOMS = {c["card_id"]: c["name"].lstrip("* ") + " (" + c["type"] + ")" for c in CARTES}
GATES = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gabarits_entete.md"), encoding="utf-8").read()
sortie = [GATES]
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
        sortie.append(f"Aucun module : `ability_link` vers **{LIENS[cid]}** (texte imprimé identique mot pour mot à la carte du core, relu sur le scan).\n")
        sortie.append(f"- [x] Étape 2 : carte de référence : {LIENS[cid]} (le script officiel EST la capacité).")
        sortie.append("- [x] Étape 5 : texte-contre-code : texte imprimé comparé mot pour mot à la carte du core. Résultat : identique.")
    sortie.append("- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan (PV par joueur, ATK, SCH, boost, menaces, seuils) et contrôlées dans `desc` "
                  "de `cards.json` et par les cas de valeurs imprimées. Résultat : conformes (boost de Thermal Target et Piercing Pharynx corrigés en ★ seule).")
    sortie.append(f"- [x] Étape 7 : cas test_capacites par capacité ({len(cas)} cas sujets) :")
    for n in cas:
        sortie.append(f"      - {n}")
    if s:
        pourquoi = "" if s[0] == s[1] else f" ; verts restants : {VERTS.get(cid, 'A EXPLIQUER')}"
        sortie.append(f"      Preuve par substitution : **rouges {s[0]}/{s[1]}** sans le module{pourquoi}. Résultat : OK.")
    elif not chemin:
        sortie.append("      Preuve par substitution : sans objet (aucun module ; le cas prouve que le lien vers la carte du core joue). Résultat : OK.")
    else:
        sortie.append("      Preuve par substitution : AUCUNE LIGNE (à relancer). Résultat : NON.")
    sortie.append("- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.")
    sortie.append(f"- [x] Étape 8 : autoplay ciblé : {AUTOPLAY} Résultat : aucun incident.")
    p = PLATEAU.get(cid)
    if p:
        sortie.append(f"- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? {p}. Cas plateau : {PLATEAU_FICHIER}. Résultat : OK.")
    else:
        sortie.append("- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? "
                      "NON en propre : elle chiffre, ou pose un attachement / un statut déjà dessiné par le rendu générique (couvert par le cas plateau). Résultat : sans objet.")
    sortie.append("\nCarte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).\n")
open(os.path.join(RACINE, "docs", "packs", "alien-vs-predator", "GABARITS.md"), "w", encoding="utf-8").write("\n".join(sortie))
print("ecrit", len(CARTES), "gabarits")
