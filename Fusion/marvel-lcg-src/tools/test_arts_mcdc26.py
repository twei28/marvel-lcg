#!/usr/bin/env python3
"""Verifie le branchement des « Full Art Reprints » MC/DC 2026 (code d'art `mcdc26`).

    python3 tools/test_arts_mcdc26.py                 # fichiers et donnees
    python3 tools/test_arts_mcdc26.py --http 8765     # + chaque art servi par un moteur deja lance

Controle : chaque carte declaree `mcdc26` existe dans cards.json (officielle, pas
une exclusive de serie), son image `assets/pics/<id>_mcdc26.jpg` existe (le
chargeur d'images exige l'extension), est un JPEG 615x882, et reste legere ;
les tables du plateau et de la preparation sont alignees sur la source.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
CODE = "mcdc26"
TAILLE = (615, 882)
POIDS_MAX = 400 * 1024


def cartes_du_jeu():
    d = json.load(open(RACINE / "data" / "cards.json", encoding="utf-8"))
    out = {}
    for v in d.values():
        if isinstance(v, list):
            for c in v:
                if isinstance(c, dict) and c.get("card_id"):
                    out[c["card_id"]] = c
    return out


def main():
    from PIL import Image
    arts = json.load(open(RACINE / "data" / "arts_alternatifs.json", encoding="utf-8"))
    jeu = cartes_du_jeu()
    ids = sorted(i for i, codes in arts["cartes"].items() if CODE in codes)
    assert len(ids) >= 38, f"attendu au moins 38 cartes {CODE}, trouve {len(ids)}"
    exclusifs = {s for serie in arts["series"].values() for s in serie["sets_exclusifs"]}
    http = None
    if "--http" in sys.argv:
        http = int(sys.argv[sys.argv.index("--http") + 1])
    for i in ids:
        assert i in jeu, f"{i} absente de cards.json"
        assert jeu[i].get("set_name") not in exclusifs, f"{i} est une exclusive de serie"
        f = RACINE / "assets" / "pics" / f"{i}_{CODE}.jpg"
        assert f.is_file(), f"image absente : {f}"
        assert f.stat().st_size < POIDS_MAX, f"{f.name} pese {f.stat().st_size} octets"
        with Image.open(f) as im:
            assert im.format == "JPEG" and im.size == TAILLE, (f.name, im.format, im.size)
        if http:
            r = urllib.request.urlopen(f"http://127.0.0.1:{http}/{i}_{CODE}", timeout=20)
            data = r.read()
            assert r.status == 200 and data[:3] == b"\xff\xd8\xff", f"{i}_{CODE} : reponse HTTP non JPEG"
            assert len(data) > 5000, f"{i}_{CODE} : image vide"
    r = subprocess.run([sys.executable, str(ICI / "generer_arts_cartes.py"), "--verifier"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    print(f"OK : {len(ids)} arts {CODE} (fichiers JPEG {TAILLE[0]}x{TAILLE[1]}, tables alignees"
          + (f", servis par le moteur :{http}" if http else "") + ")")


main()
