#!/usr/bin/env python3
"""Verifie le branchement des reskins du heros BINARY (Galactic Storm, Kajislav), code d'art `binary`.

    python3 tools/test_arts_binary.py                 # fichiers et donnees
    python3 tools/test_arts_binary.py --http 8765     # + chaque art servi par un moteur deja lance

Controle : 19 cartes officielles declarees `binary` (Avengers Mansion 01091 exclue tant que la
question Q2 n'est pas tranchee), chacune presente dans cards.json, son image
`assets/pics/<id>_binary.jpg` (JPEG 615x882, 882x615 pour une manigance de joueur) ; la serie
`binary` designe le heros gs001 ; la collection de ressources `binary` (01088-01090) a ses trois
images et figure dans les DEUX tables (plateau `variantes.ts`, preparation `app.js`) ; les tables
d'arts sont alignees sur la source.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
CODE = "binary"
ATTENDUES = {"43035", "49022", "16045", "43018", "42023", "54016", "43037", "06017", "16024", "41019",
             "33032", "56013", "43036", "13013", "12030", "43034", "40204", "01084", "43021"}
PAYSAGE = {"43018", "43021"}
EXCLUES = {"01091"}


def cartes_du_jeu():
    d = json.load(open(RACINE / "data" / "cards.json", encoding="utf-8"))
    return {c["card_id"]: c for v in d.values() if isinstance(v, list) for c in v
            if isinstance(c, dict) and c.get("card_id")}


def main():
    from PIL import Image
    arts = json.load(open(RACINE / "data" / "arts_alternatifs.json", encoding="utf-8"))
    jeu = cartes_du_jeu()
    ids = {i for i, codes in arts["cartes"].items() if CODE in codes}
    assert ids == ATTENDUES, f"arts {CODE} : en trop {sorted(ids - ATTENDUES)}, manquants {sorted(ATTENDUES - ids)}"
    assert not (ids & EXCLUES), "une carte en question est branchee"
    serie = arts["series"].get(CODE)
    assert serie and serie["heros_cartes"] == ["gs001"] and serie["heros_ids"] == ["binary"], serie
    assert jeu.get("gs001a") and jeu.get("gs001b"), "le heros Binary est absent de cards.json"
    http = int(sys.argv[sys.argv.index("--http") + 1]) if "--http" in sys.argv else None
    for i in sorted(ids) + ["01088", "01089", "01090"]:
        assert i in jeu, f"{i} absente de cards.json"
        f = RACINE / "assets" / "pics" / f"{i}_{CODE}.jpg"
        assert f.is_file(), f"image absente : {f}"
        taille = (882, 615) if i in PAYSAGE else (615, 882)
        with Image.open(f) as im:
            assert im.format == "JPEG" and im.size == taille, (f.name, im.format, im.size)
        if http:
            r = urllib.request.urlopen(f"http://127.0.0.1:{http}/{i}_{CODE}", timeout=20)
            assert r.status == 200 and r.read()[:3] == b"\xff\xd8\xff", f"{i}_{CODE} : reponse non JPEG"
    ts = (RACINE.parent.parent / "ui-app" / "src" / "board" / "variantes.ts").read_text(encoding="utf-8")
    js = (RACINE / "public" / "js" / "prepare" / "app.js").read_text(encoding="utf-8")
    assert "binary: ['01088_binary', '01089_binary', '01090_binary']" in ts, "collection absente de variantes.ts"
    assert '{ code: "binary", nom: "Binary", apercu: "01089_binary" }' in js, "collection absente de app.js"
    r = subprocess.run([sys.executable, str(ICI / "generer_arts_cartes.py"), "--verifier"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    print(f"OK : {len(ids)} arts {CODE} + 3 ressources, serie du heros gs001, tables alignees"
          + (f", servis par le moteur :{http}" if http else ""))


main()
