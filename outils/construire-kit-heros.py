#!/usr/bin/env python3
"""Construit le MANUEL et le ZIP du kit de creation de HEROS (20/10/2026).

    python3 outils/construire-kit-heros.py            # manuel + zip
    python3 outils/construire-kit-heros.py --sans-zip # manuel seulement

Meme methode que `construire-kit-campagne.py` (dont ce script reutilise le moteur de directives) : les chapitres
sont ecrits a la main dans `docs/kit-heros-ia/parties/*.md`, et chaque exemple de code ou de donnees y est une
DIRECTIVE qui recopie le fichier REEL du depot au moment de la construction. Aucun exemple n'est retape.

Directives de `construire-kit-campagne.py` reprises telles quelles : FICHIER, EXTRAIT, BLOC, SECTION, TITRES, CARTE,
SETSINFO, PREFIXES, PREFIXE, TEXTESFR, PUZZLE, JSONCLE, JSONCLES.

Directives propres aux heros :
  {{STATS:}}                    chiffres mesures sur les decks de depart et les cartes (tableau)
  {{DECKBUILDING:}}             les `metadata.deckbuilding` de tous les decks qui en ont
  {{TABLECARTES:pack}}          le plan de cartes d'un pack (id, type, nom, classe, cout, set)
  {{LIGNE:chemin|motif|lang}}   la premiere ligne d'un fichier qui CONTIENT `motif`
  {{ENTREE:chemin|cle}}         l'entree `"<cle>": { ... }` d'un fichier de biographies (heros-info.js)
"""
import collections
import glob
import importlib.util
import io
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
KIT = os.path.join(RACINE, "docs", "kit-heros-ia")
ZIP = os.path.join(RACINE, "kit-heros-ia.zip")
MOTEUR = "Fusion/marvel-lcg-src"


def charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, fichier))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


KC = charger("construire_kit_campagne", "construire-kit-campagne.py")
KC.KIT = KIT
KC.PARTIES = os.path.join(KIT, "parties")

PROPRES = re.compile(r"^\{\{(STATS|DECKBUILDING|TABLECARTES|LIGNE|ENTREE):([^}]*)\}\}\s*$")


def decks():
    sortie = {}
    for f in sorted(glob.glob(os.path.join(RACINE, MOTEUR, "deck", "starter", "*.json"))):
        sortie[os.path.basename(f)[:-5]] = json.loads(KC.lire(os.path.relpath(f, RACINE)))
    return sortie


def stats():
    d = decks()
    cartes = KC.cartes()
    n = len(d)
    taille = collections.Counter(len(v.get("hero_deck", [])) for v in d.values())
    nemesis = collections.Counter(len(v.get("nemesis_set", [])) for v in d.values())
    obligations = collections.Counter(len(v.get("obligations", [])) for v in d.values())
    pdeck = collections.Counter(len(v.get("player_deck", [])) for v in d.values())
    exemplaires = collections.Counter(
        max(collections.Counter(v.get("hero_deck", [])).values() or [0]) for v in d.values())
    meta = collections.Counter(k for v in d.values() for k in (v.get("metadata") or {}))
    formes = collections.Counter(len(v["hero"][0].split(",")) for v in d.values() if v.get("hero"))
    variantes = sum(1 for v in d.values() if (v.get("metadata") or {}).get("variante_de"))
    fan = sum(1 for v in d.values() if (cartes.get(v["hero"][0].split(",")[0]) or {}).get("custom"))

    def ligne(titre, compteur):
        return "| %s | %s |" % (titre, ", ".join("%s : %d" % (k, c) for k, c in sorted(compteur.items())))
    return "\n".join([
        "| Mesure sur les %d decks de départ | Valeurs : nombre de decks |" % n,
        "|---|---|",
        ligne("cartes dans `hero_deck`", taille),
        ligne("plus grand nombre d'exemplaires d'un titre", exemplaires),
        ligne("cartes dans `obligations`", obligations),
        ligne("cartes dans `nemesis_set`", nemesis),
        ligne("cartes dans `player_deck`", pdeck),
        ligne("faces listées dans `hero`", formes),
        "| héros dont la face héros porte `custom` (fan-made) | %d |" % fan,
        "| decks qui sont des **variantes** (`variante_de`) | %d |" % variantes,
        "| clés de `metadata` les plus courantes | %s |" % ", ".join(
            "`%s` ×%d" % (k, c) for k, c in meta.most_common(8)),
    ]) + "\n"


def deckbuilding():
    sortie = {k: v["metadata"]["deckbuilding"] for k, v in decks().items() if (v.get("metadata") or {}).get("deckbuilding")}
    return KC.bloc(json.dumps(sortie, ensure_ascii=False, indent=2), "json")


def table_cartes(pack):
    donnees = json.loads(KC.lire(MOTEUR + "/data/cards.json"))
    if pack not in donnees:
        raise SystemExit("directive TABLECARTES : pack inconnu : %s" % pack)
    lignes = ["| card_id | type | nom | classe | coût | ressource | set_name |", "|---|---|---|---|---|---|---|"]
    for c in donnees[pack]:
        if "card_id" not in c:
            continue
        d = c.get("desc") or {}
        lignes.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            c["card_id"], c.get("type", ""), (c.get("name") or "").replace("|", "/"), d.get("Class", ""),
            d.get("Cost", ""), d.get("RES", ""), c.get("set_name", "")))
    return "\n".join(lignes) + "\n"


def entree(chemin, cle):
    texte = KC.lire(chemin).replace("\r\n", "\n")
    m = re.search(r'^    "%s": \{\n.*?^    \},?\n' % re.escape(cle), texte, re.M | re.S)
    if not m:
        raise SystemExit("directive ENTREE : cle introuvable dans %s : %s" % (chemin, cle))
    return "*Entrée `%s` de `%s`.*\n\n%s" % (cle, chemin, KC.bloc(m.group(0), "javascript"))


def ligne_motif(chemin, motif, langage):
    for l in KC.lire(chemin).replace("\r\n", "\n").split("\n"):
        if motif in l:
            return "*Ligne de `%s`.*\n\n%s" % (chemin, KC.bloc(l, langage or KC.langage_de(chemin)))
    raise SystemExit("directive LIGNE : motif introuvable dans %s : %r" % (chemin, motif))


EXPANSER_CAMPAGNE = KC.expanser


def expanser(ligne):
    m = PROPRES.match(ligne)
    if not m:
        return EXPANSER_CAMPAGNE(ligne)
    genre, args = m.group(1), m.group(2).split("|")
    if genre == "STATS":
        return stats()
    if genre == "DECKBUILDING":
        return deckbuilding()
    if genre == "TABLECARTES":
        return table_cartes(args[0])
    if genre == "ENTREE":
        return entree(args[0], args[1])
    return ligne_motif(args[0], args[1], args[2] if len(args) > 2 else "")


KC.expanser = expanser


def main():
    sans_zip = "--sans-zip" in sys.argv
    parties = KC.PARTIES
    fichiers = sorted(f for f in os.listdir(parties) if f.endswith(".md"))
    manuel = KC.assembler(fichiers)
    chemin = os.path.join(KIT, "KIT-HEROS-COMPLET.md")
    with io.open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write(manuel)
    print("%s : %d lignes, %d Ko" % (chemin, manuel.count("\n") + 1, len(manuel.encode()) // 1024))
    if sans_zip:
        return 0
    sys.path.insert(0, ICI)
    zip_kit = charger("zip_kit_heros", "zip_kit_heros.py")
    zip_kit.construire(RACINE, KIT, ZIP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
