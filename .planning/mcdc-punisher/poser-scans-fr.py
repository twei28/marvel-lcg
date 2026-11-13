#!/usr/bin/env python3
"""Pose les scans FRANCAIS de la campagne « La ville ne dort jamais » (zip de l'equipe MC×DC, 13/11/2026) dans assets/pics-fr.

Relancable. Pour chaque image du zip : numero MC×DC 60NN(A|B) -> carte `puNNN(a|b)` du moteur, redimensionnee en 615x882
(portrait) ou 882x615 (paysage) et ecrite en `fr_<id>.jpg`, comme les scans des autres packs fan-made. The City (pu005) et
Never Sleeps (pu006) passent par panorama-city-fr.py (illustrations recollees). Les seconds exemplaires d'une meme carte
(6019, 6061...) n'ont pas de fiche propre : ils partagent le scan de l'original. Les images de campagne et de defi (6132-6141)
ne portent pas le numero de leur fiche : elles sont listees a part, rien n'est devine.
Usage : python3 poser-scans-fr.py <zip> [--sec]   (--sec : n'ecrit rien)
"""
import io, json, re, subprocess, sys, tempfile, zipfile
from pathlib import Path
from PIL import Image

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent.parent
MOTEUR = RACINE / "Fusion" / "marvel-lcg-src"
SORTIE = MOTEUR / "assets" / "pics-fr"
PANO = {"pu005": 0, "pu006": 1}

cartes = json.load(open(MOTEUR / "data" / "cards.json"))
def parcourir(x):
    if isinstance(x, dict):
        if "card_id" in x: yield x["card_id"]
        else:
            for v in x.values(): yield from parcourir(v)
    elif isinstance(x, list):
        for v in x: yield from parcourir(v)
ids = {c for c in parcourir(cartes) if str(c).startswith("pu")}

z = zipfile.ZipFile(sys.argv[1])
images, reste = {}, []
for nom in sorted(z.namelist()):
    m = re.search(r"/(\d{4})([AB]?) - .*\.jpg$", nom)
    if not m: continue
    cid = "pu%03d%s" % (int(m.group(1)) - 6000, m.group(2).lower())
    if cid in ids: images[cid] = nom
    else: reste.append(nom.split("/")[-1])

with tempfile.TemporaryDirectory() as tmp:
    pano = {}
    # panorama : extrait les deux scans, lance le script, relit les deux moities
    if "pu005" in images and "pu006" in images:
        for cid in PANO: (Path(tmp) / (cid + ".jpg")).write_bytes(z.read(images[cid]))
        subprocess.run([sys.executable, str(ICI / "panorama-city-fr.py"), str(Path(tmp) / "pu005.jpg"), str(Path(tmp) / "pu006.jpg"), tmp], check=True)
        pano = {"pu005": Path(tmp) / "pu005_pano.jpg", "pu006": Path(tmp) / "pu006_pano.jpg"}
    ecrits = []
    for cid, nom in sorted(images.items()):
        im = Image.open(pano[cid] if cid in pano else io.BytesIO(z.read(nom))).convert("RGB")
        taille = (882, 615) if im.width > im.height else (615, 882)
        if "--sec" not in sys.argv:
            im.resize(taille, Image.LANCZOS).save(SORTIE / ("fr_%s.jpg" % cid), quality=90)
        ecrits.append(cid)
print(len(ecrits), "scans poses")
print("ids :", ", ".join(ecrits))
print("images non associees (%d) :" % len(reste)); [print("  ", r) for r in reste]
print("cartes pu sans scan FR :", ", ".join(sorted(ids - set(ecrits))))
