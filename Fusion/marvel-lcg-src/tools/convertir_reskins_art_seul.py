#!/usr/bin/env python3
"""Convertit les reskins TMNT « SEULE l'image change » en arts alternatifs.

Regle de l'utilisateur (17/10/2026) : une carte TMNT qui ne change que
l'image de l'officielle n'est pas une carte : c'est un ART ALTERNATIF de
l'officielle. Pour chaque carte classee « art seul » par
tools/classer_reskins_tmnt.py, ce script :

  1. retire son entree de data/cards.json (checksum recalcule) ;
  2. la declare dans data/arts_alternatifs.json (officielle -> ["tmnt"]) ;
  3. COPIE son image `assets/pics/<id TMNT>.jpg` en `<officielle>_tmnt.jpg`
     (copie, jamais deplacement : assets/pics est partage entre les worktrees ;
     le fichier d'origine se supprime a la main une fois le tout verifie) ;
  4. regenere les tables (tools/generer_arts_cartes.py) ;
  5. LISTE les autres fichiers qui citent encore ces identifiants (cas de test,
     textes FR, numerotation...) : a reprendre a la main, rien n'y est reecrit.

Par defaut c'est un essai a blanc. Usage :

    python3 tools/convertir_reskins_art_seul.py                  # essai : ce qui serait fait
    python3 tools/convertir_reskins_art_seul.py --ecrire         # le fait
    python3 tools/convertir_reskins_art_seul.py --racine COPIE --ecrire   # sur une copie

`--racine` : une arborescence qui contient data/ (et tools/ pour le TSV) ; les
images y sont lues dans <racine>/assets/pics (rien n'est ecrit hors de la racine).
Relancer apres une nouvelle retouche d'une carte est sans danger : les cartes
deja converties n'existent plus dans cards.json et sont ignorees.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import classer_reskins_tmnt as classeur  # noqa: E402

CODE_ART = "tmnt"
RESSOURCES_DOUBLES = {"01088", "01089", "01090"}


def checksum(d):
    """Meme calcul que le moteur (Types.DictChecksum) : sha256 du JSON trie, sans la cle checksum."""
    sans = {k: v for k, v in d.items() if k != "checksum"}
    return hashlib.sha256(json.dumps(sans, sort_keys=True).encode()).hexdigest()


def ecrire_json(chemin, d):
    chemin.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def principal():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--racine", type=Path, default=ICI.parent, help="racine du moteur (defaut : celle de ce script)")
    ap.add_argument("--ecrire", action="store_true", help="applique (sinon essai a blanc)")
    ap.add_argument("--sans-images", action="store_true", help="ne copie pas les images")
    a = ap.parse_args()
    racine = a.racine.resolve()
    cartes_json = racine / "data" / "cards.json"
    arts_json = racine / "data" / "arts_alternatifs.json"
    tsv = racine / "tools" / "tmnt_aspects_numerotation.tsv"
    pics = racine / "assets" / "pics"

    brut = json.loads(cartes_json.read_text(encoding="utf-8"))
    cartes = {}
    for v in brut.values():
        if isinstance(v, list):
            for c in v:
                if isinstance(c, dict) and c.get("card_id"):
                    cartes[c["card_id"]] = c
    classement = classeur.classer(cartes, classeur.lire_origines(tsv))
    # Les trois ressources doubles (Energy, Genius, Strength) suivent le precedent
    # des re-skins de pack (Gwenpool, Howard...) : elles RESTENT des cartes de
    # cards.json et forment la collection « tmnt » de COLLECTIONS (variantes.ts,
    # app.js), choisie comme les autres collections de ressources.
    art_seul = [(cid, nom, off) for cid, nom, off, ecarts in classement
                if not ecarts and off not in RESSOURCES_DOUBLES]
    print(f"{len(classement)} reskins encore dans cards.json, dont {len(art_seul)} « art seul »")
    if not art_seul:
        return 0

    # Gardes-fous : l'officielle existe, n'a pas deja ce code, et le lien d'aptitude concorde.
    for cid, nom, off in art_seul:
        lien = cartes[cid].get("ability_link")
        if lien not in (None, off):
            sys.exit(f"{cid} : ability_link={lien} differe de l'officielle {off} : a verifier a la main")
        if off in cartes and cartes[off].get("ability_link"):
            sys.exit(f"{off} est elle-meme un lien : cible inattendue")

    retirees = {cid for cid, _, _ in art_seul}
    # Une autre carte ne doit pas pointer vers une carte retiree.
    for c in cartes.values():
        for cle in ("ability_link", "full_link", "multiverse_of"):
            if c.get(cle) in retirees and c["card_id"] not in retirees:
                sys.exit(f"{c['card_id']}.{cle} pointe vers {c[cle]}, qui serait retiree")

    arts = json.loads(arts_json.read_text(encoding="utf-8"))
    for cid, nom, off in art_seul:
        image = pics / f"{cid}.jpg"
        cible = pics / f"{off}_{CODE_ART}.jpg"
        etat_img = "image absente" if not image.exists() else ("deja copiee" if cible.exists() else "a copier")
        print(f"  {cid} {nom} -> {off}_{CODE_ART}  [{etat_img}]")

    if not a.ecrire:
        print("essai a blanc : rien n'est ecrit (--ecrire pour appliquer)")
        return 0

    for cid, nom, off in art_seul:
        codes = arts["cartes"].setdefault(off, [])
        if CODE_ART not in codes:
            codes.append(CODE_ART)
        if not a.sans_images:
            image, cible = pics / f"{cid}.jpg", pics / f"{off}_{CODE_ART}.jpg"
            if image.exists() and not cible.exists():
                shutil.copy2(image, cible)
    arts["cartes"] = dict(sorted(arts["cartes"].items()))
    ecrire_json(arts_json, arts)

    for cle, v in brut.items():
        if isinstance(v, list):
            brut[cle] = [c for c in v if not (isinstance(c, dict) and c.get("card_id") in retirees)]
    brut["checksum"] = checksum(brut)
    cartes_json.write_text(json.dumps(brut, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"cards.json : {len(retirees)} entrees retirees, checksum recalcule")

    # Tables generees (le generateur lit data/arts_alternatifs.json de SA racine).
    if racine == ICI.parent:
        subprocess.run([sys.executable, str(ICI / "generer_arts_cartes.py")], check=True)
    else:
        print("racine differente : generateur non lance (tables du depot inchangees)")

    # Ce qui cite encore ces identifiants : a reprendre a la main.
    print("\nFichiers qui citent encore une carte retiree (a reprendre) :")
    depot = racine.parent.parent if (racine.parent.parent / "ui-app").is_dir() else racine
    rg = subprocess.run(["grep", "-rIlE", "|".join(sorted(retirees)),
                         "--exclude-dir=node_modules", "--exclude-dir=.git", "--exclude-dir=.game-src",
                         "--exclude-dir=assets", "--exclude=cards.json", "--exclude=arts_alternatifs.json",
                         str(racine), *([str(depot / "ui-app" / "src")] if depot != racine else [])],
                        capture_output=True, text=True)
    for ligne in sorted(set(rg.stdout.split("\n"))):
        if ligne:
            print("  ", ligne)
    return 0


if __name__ == "__main__":
    sys.exit(principal())
