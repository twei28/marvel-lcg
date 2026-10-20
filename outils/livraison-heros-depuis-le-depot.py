#!/usr/bin/env python3
"""Reconstitue, A PARTIR DU DEPOT, la « livraison » d'un HEROS deja integre (20/10/2026).

    python3 outils/livraison-heros-depuis-le-depot.py <pack> <deck> <dossier sortie> [--officiel]

    <pack>  la cle du pack dans data/cards.json            (lockjaw, ant, iron_fist, harry_osborn)
    <deck>  l'identifiant du deck de depart du heros       (deck/starter/<deck>.json)

POURQUOI
--------
Le kit de creation de heros dit a une autre IA comment LIVRER ses fichiers (`livraison/`, voir le chapitre 9 du
manuel). Pour que l'exemple soit exact et que le verificateur (`verifier-livraison-heros.py`) soit CALIBRE sur du
vrai contenu, on refait, pour un heros qui marche en jeu, le dossier qu'une IA aurait du livrer : fragments de
`cards.json` et `sets_info.json`, deck de depart (+ variantes), set nemesis, scripts, textes francais, biographie,
replique de recrutement, prefixe, cas de test, et les fichiers de suivi.

Les fichiers de suivi sont GENERES : ils montrent le FORMAT attendu, ils ne sont pas la preuve qu'un humain les a
relus.
"""
import argparse
import glob
import io
import json
import os
import re
import shutil
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")


def lire(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as f:
        return f.read()


def ecrire(chemin, contenu):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write(contenu)


def ecrire_json(chemin, valeur):
    ecrire(chemin, json.dumps(valeur, ensure_ascii=False, indent=4) + "\n")


def extraire_textes_fr(ids):
    lignes = lire(os.path.join(RACINE, "ui-app", "src", "board", "textes-fr-fanmade.ts")).split("\n")
    sortie = []
    for i, l in enumerate(lignes):
        m = re.match(r"^  '([^']+)':", l)
        if m and m.group(1) in ids:
            if i and lignes[i - 1].lstrip().startswith("//"):
                sortie.append(lignes[i - 1])
            sortie.append(l)
    return "\n".join(sortie) + "\n" if sortie else None


def extraire_bio(card_id):
    texte = lire(os.path.join(MOTEUR, "public", "js", "prepare", "heros-info.js"))
    m = re.search(r'^    "%s": \{\n.*?^    \},?\n' % re.escape(card_id), texte, re.M | re.S)
    return m.group(0) if m else None


def extraire_replique(deck):
    texte = lire(os.path.join(MOTEUR, "public", "js", "prepare", "repliques-heros.js"))
    m = re.search(r"^    %s: \[.*\],?\n" % re.escape(deck), texte, re.M)
    return m.group(0) if m else None


def role(f):
    if f.startswith("data/cards."):
        return "cartes du pack"
    if f.startswith("data/sets_info."):
        return "entree de l'index des packs (liste `heroes`)"
    if f.startswith("data/nemesis/"):
        return "set nemesis nomme (facultatif)"
    if f.startswith("deck/starter/"):
        return "deck de depart du heros (variante comprise)"
    if f.endswith("__init__.py"):
        return "helpers partages"
    if f.startswith("src/"):
        return "script de carte"
    if f.startswith("textes-fr/"):
        return "textes francais"
    if f.startswith("tools/prefixes."):
        return "prefixe fan-made"
    if f.startswith("tools/cas/"):
        return "cas de test de capacite"
    if f.startswith("tools/decks-de-test"):
        return "moitie d'aspect de TEST (harnais seulement)"
    if f.startswith("public/js/prepare/heros-info"):
        return "biographie du heros"
    if f.startswith("public/js/prepare/repliques"):
        return "replique de recrutement"
    return ""


def construire(pack, deck, sortie, officiel):
    if os.path.exists(sortie):
        shutil.rmtree(sortie)
    integ = os.path.join(sortie, "integration")
    donnees = json.loads(lire(os.path.join(MOTEUR, "data", "cards.json")))
    cartes = donnees[pack]
    ids = {c["card_id"] for c in cartes if "card_id" in c}
    ecrire_json(os.path.join(integ, "data", "cards.%s.fragment.json" % pack), {pack: cartes})
    infos = json.loads(lire(os.path.join(MOTEUR, "data", "sets_info.json")))
    cle_info = next(k for k, v in infos.items() if isinstance(v, dict) and v.get("name") == pack)
    cle_neutre = re.sub(r"^\d+\.", "N.", cle_info) if not officiel else cle_info
    ecrire_json(os.path.join(integ, "data", "sets_info.%s.fragment.json" % pack), {cle_neutre: infos[cle_info]})
    # le deck de depart et ses variantes (second deck replie sous le premier : `metadata.variante_de`)
    chemin_deck = os.path.join(MOTEUR, "deck", "starter", deck + ".json")
    d = json.loads(lire(chemin_deck))
    ecrire_json(os.path.join(integ, "deck", "starter", deck + ".json"), d)
    for f in sorted(glob.glob(os.path.join(MOTEUR, "deck", "starter", "*.json"))):
        v = json.loads(lire(f))
        if (v.get("metadata") or {}).get("variante_de") == deck:
            ecrire_json(os.path.join(integ, "deck", "starter", os.path.basename(f)), v)
    nem = os.path.join(MOTEUR, "data", "nemesis", deck + "_nemesis.json")
    if os.path.exists(nem):
        ecrire_json(os.path.join(integ, "data", "nemesis", deck + "_nemesis.json"), json.loads(lire(nem)))
    # scripts
    src = os.path.join(MOTEUR, "src", "cards", "pack", pack)
    for dd, ds, fs in os.walk(src):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(dd, f), src)
                ecrire(os.path.join(integ, "src", "cards", "pack", pack, rel), lire(os.path.join(dd, f)))
    # textes francais (les heros officiels recents en ont aussi : Iron Fist)
    fr = extraire_textes_fr(ids)
    if fr:
        ecrire(os.path.join(integ, "textes-fr", "%s.fragment.txt" % pack), fr)
    if not officiel:
        prefixes = json.loads(lire(os.path.join(MOTEUR, "tools", "prefixes_fanmade.json")))["prefixes"]
        for p, v in prefixes.items():
            if v.get("pack") == pack:
                ecrire_json(os.path.join(integ, "tools", "prefixes.%s.fragment.json" % pack), {p: v})
    # biographie + replique
    face_heros = d["hero"][0].split(",")[0]
    bio = extraire_bio(face_heros)
    if bio:
        ecrire(os.path.join(integ, "public", "js", "prepare", "heros-info.fragment.js"), bio)
    rep = extraire_replique(deck)
    if rep:
        ecrire(os.path.join(integ, "public", "js", "prepare", "repliques-heros.fragment.js"), rep)
    # cas de test (un fichier dedie, quand il existe) et moitie d'aspect de test
    cas = os.path.join(MOTEUR, "tools", "cas", deck + ".py")
    if os.path.exists(cas):
        ecrire(os.path.join(integ, "tools", "cas", deck + ".py"), lire(cas))
    dt = os.path.join(MOTEUR, "tools", "decks-de-test.json")
    if os.path.exists(dt):
        moitie = json.loads(lire(dt)).get("decks", {}).get(face_heros)
        if moitie:
            ecrire_json(os.path.join(integ, "tools", "decks-de-test.fragment.json"), {"decks": {face_heros: moitie}})
    # fichiers de suivi
    fichiers = []
    for dd, ds, fs in os.walk(integ):
        for f in sorted(fs):
            fichiers.append(os.path.relpath(os.path.join(dd, f), integ).replace("\\", "/"))
    fichiers.sort()
    manifeste = ["# MANIFESTE (genere depuis le depot : forme attendue)", "",
                 "| Chemin (dans integration/) | Role |", "|---|---|"]
    for f in fichiers:
        manifeste.append("| %s | %s |" % (f, role(f)))
    manifeste += ["", "Cartes (faces) : %d. Scripts : %d. Deck(s) de depart : %d." % (
        len(cartes), sum(1 for f in fichiers if f.startswith("src/") and re.search(r"/[0-9a-z]+\.py$", f)),
        sum(1 for f in fichiers if f.startswith("deck/starter/")))]
    ecrire(os.path.join(sortie, "MANIFESTE.md"), "\n".join(manifeste) + "\n")
    img = ["# images.md (genere depuis le depot)", "", "| card_id | fichier | taille |", "|---|---|---|"]
    try:
        from PIL import Image  # facultatif
    except Exception:
        Image = None
    for c in cartes:
        cid = c.get("card_id")
        if not cid or "full_link" in c:
            continue
        trouve = None
        for ext in ("jpg", "png", "webp"):
            p = os.path.join(MOTEUR, "assets", "pics", "%s.%s" % (cid, ext))
            if os.path.exists(p):
                trouve = p
                break
        taille = ""
        if trouve and Image:
            try:
                w, h = Image.open(trouve).size
                taille = "%dx%d" % (w, h)
            except Exception:
                taille = ""
        img.append("| %s | %s | %s |" % (cid, os.path.basename(trouve) if trouve else "(absente du depot)", taille))
    ecrire(os.path.join(sortie, "images.md"), "\n".join(img) + "\n")
    auteurs = sorted({c.get("custom") for c in cartes if c.get("custom")})
    ecrire(os.path.join(sortie, "CREDITS.md"), "# CREDITS\n\nAuteur(s) (cle `custom` des cartes) : %s\n" % (", ".join(auteurs) or "(contenu officiel)"))
    gab = os.path.join(RACINE, "docs", "packs", deck + "_cartes.md")
    gabarits = "# GABARITS\n\n(Exemple de forme : manuel, chapitre 8.)\n"
    if os.path.exists(gab):
        gabarits = "# GABARITS (gabarits PROCESSUS-CARTE reels de ce heros, copies du depot)\n\n" + \
                   re.sub(r"[^\n]*Claude-Session:[^\n]*\n?", "", lire(gab))
    ecrire(os.path.join(sortie, "GABARITS.md"), gabarits)
    for nom, txt in (("QUESTIONS.md", "# QUESTIONS\n\n(Aucune : heros deja integre. Format : manuel, chapitre 9.)\n"),
                     ("BESOINS-MOTEUR.md", "# BESOINS-MOTEUR\n\n(Aucun : heros deja integre. Format : manuel, chapitre 9.)\n"),
                     ("A_FAIRE_CLAUDE.md", "# A_FAIRE_CLAUDE\n\n(Aucun marqueur : heros deja integre.)\n"),
                     ("AUTO-VERIFICATION.md", "# AUTO-VERIFICATION\n\n(Exemple de forme : manuel, chapitre 9.)\n")):
        ecrire(os.path.join(sortie, nom), txt)
    print("livraison de %s ecrite dans %s (%d fichiers dans integration/)" % (pack, sortie, len(fichiers)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack")
    ap.add_argument("deck")
    ap.add_argument("sortie")
    ap.add_argument("--officiel", action="store_true")
    a = ap.parse_args()
    construire(a.pack, a.deck, a.sortie, a.officiel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
