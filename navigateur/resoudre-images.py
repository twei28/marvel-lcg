#!/usr/bin/env python3
"""Calcule, AVEC LE CODE DU MOTEUR, l'image que le jeu classique renvoie pour chaque nom, pour que
play.<domaine> (hebergement statique) serve exactement la meme.

    cd Fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 ../../navigateur/resoudre-images.py <sortie>

POURQUOI (07/10/2026). Le moteur classique ne sert pas des fichiers : il RESOUT un nom (engine/file/cache.py,
Cache.LoadImage) a travers une chaine -- quatre dossiers dans l'ordre (pics, pics-fr, textures, cache), trois
extensions (.webp, .jpg, .png), les images liees (`pic_id`, `full_link`), le repli `fr_X` -> `X`, le
telechargement des scans officiels manquants, et enfin une carte DESSINEE (nom, type, texte) pour ce qui n'a
pas de scan. Les vignettes et la HD ont leurs propres chaines. Un serveur statique ne sait rien de tout ca :
chaque maillon oublie dans Caddy etait une image absente sur play.

Plutot que de recopier cette logique, on fait tourner LE CODE DU MOTEUR sur tous les noms possibles et on note
ce qu'il a lu. Sortie :
    <sortie>/resolution.json   { route: { nom: "dossier/fichier" } }   route = image | vignette | hd
    <sortie>/generes/<route>/<nom>.<ext>   les images que le moteur FABRIQUE (carte dessinee, scan telecharge)
`navigateur/installer-images.py` en fait, sur le serveur, des liens vers les scans deja copies.
"""
import json, os, re, sys

os.environ["RELEASE"] = "1"
sortie = os.path.abspath(sys.argv[1])
os.makedirs(sortie, exist_ok=True)
sys.path.insert(0, os.path.abspath("src"))

from core import *  # noqa: F401,F403  (initialise le moteur comme au lancement)
from engine.file import Cache, FileManager
from engine.file import cache as module_cache
from engine.lib import ImageLib, ImageCreator
from cards.database import CardsDB
# Le debut d'Engine.Initialize, sans le serveur (qui prendrait le port du jeu) : version, configuration
# (launch.json), traductions, generateur d'images, base des cartes. Nos reglages viennent APRES.
from engine.lib import Ver
from engine.config import ConfigVariables
from engine.lib import TransText
Ver.Initialize()
ConfigVariables.Initialize()
TransText.Initialize()
ImageCreator.Initialize()
CardsDB.Initialize()

# Les telechargements (scans officiels absents du disque) atterrissent DANS LA SORTIE, jamais dans assets/.
CACHE_SORTIE = os.path.join(sortie, "cache-telecharge")
os.makedirs(CACHE_SORTIE, exist_ok=True)
DOSSIERS = {"pics": "./assets/pics/", "pics-fr": "./assets/pics-fr/", "textures": "./assets/textures/",
            "cache": "./assets/cache/", "vignettes": "./assets/vignettes/", "pics-hd": "./assets/pics-hd/"}

# Le dossier des telechargements et celui de la HD sont des COPIES dans la sortie : le moteur y ecrit
# (scans officiels manquants, scans HD, faces HD croisees redressees), et rien ne doit toucher assets/.
import shutil
for cle, cible in (("cache", CACHE_SORTIE), ("pics-hd", os.path.join(sortie, "hd"))):
    if not os.path.isdir(cible) or not os.listdir(cible):
        shutil.copytree(DOSSIERS[cle], cible, dirs_exist_ok=True)
ORIGINE = dict(DOSSIERS)
DOSSIERS["cache"] = CACHE_SORTIE + "/"
DOSSIERS["pics-hd"] = os.path.join(sortie, "hd") + "/"
module_cache.CACHE_FOLDER.value = DOSSIERS["cache"]
module_cache.HD_FOLDER.value = DOSSIERS["pics-hd"]

module_cache.IMAGE_SERVERS.value = [
    "https://cerebrodatastorage.blob.core.windows.net/cerebro-cards/official/{card_id:U}.jpg",
    "https://marvelcdb.com/bundles/cards/{card_id}.jpg",
]
module_cache.SAVE_EMPTY_IMAGE.value = False
ImageCreator.show_image_text = True

# Ce que le moteur LIT, pour chaque resolution : le dernier fichier ouvert en lecture.
lu = []
ouvrir_origine = FileManager.OpenFile
def ouvrir(path, *a, **k):
    if k.get("read"):
        lu.append(path)
    return ouvrir_origine(path, *a, **k)
FileManager.OpenFile = ouvrir
ImageLib.TryRotateImage = staticmethod(lambda data: data)   # le redressement est fait par preparer-scans.py


def relatif(chemin):
    chemin = os.path.normpath(chemin).replace("\\", "/")
    for cle, base in DOSSIERS.items():
        b = os.path.normpath(base).replace("\\", "/") + "/"
        if chemin.startswith(b):
            return cle + "/" + chemin[len(b):]
    return None

def ext_de(octets):
    if octets[1:4] == b"PNG": return "png"
    if octets[:4] == b"RIFF" and octets[8:12] == b"WEBP": return "webp"
    if octets[:5] == b"<?xml" or octets[:4] == b"<svg": return "svg"
    return "jpg"

def resoudre(route, nom, fonction):
    Cache.cache.clear()
    del lu[:]
    data = fonction(nom)
    if lu:
        r = relatif(lu[-1])
        # Un fichier lu dans une COPIE (cache, hd) n'est sur le serveur que s'il venait d'assets/ : sinon il vient
        # d'etre telecharge, et il part avec les images fabriquees.
        if r and (not r.startswith(("cache/", "pics-hd/")) or os.path.isfile(os.path.join(ORIGINE[r.split("/")[0]], r.split("/", 1)[1]))):
            return r
    # Rien lu sur le disque : image telechargee ou dessinee. On garde les octets.
    dossier = os.path.join(sortie, "generes", route)
    os.makedirs(dossier, exist_ok=True)
    fichier = f"{nom.replace('/', '__')}.{ext_de(data)}"
    with open(os.path.join(dossier, fichier), "wb") as f:
        f.write(data)
    return f"generes/{route}/{fichier}"

# L'univers des noms : tout ce qui existe sur le disque, toutes les cartes connues, tous les liens, et leur
# version fr_.
noms = set()
for cle in ("pics", "pics-fr", "textures", "cache"):
    base = DOSSIERS[cle]
    for racine, _, fichiers in os.walk(base):
        for f in fichiers:
            souche, ext = os.path.splitext(f)
            if ext.lower() not in (".webp", ".jpg", ".png"):
                continue
            rel = os.path.relpath(os.path.join(racine, souche), base).replace("\\", "/")
            noms.add(rel)
cartes = set(CardsDB.papers.keys()) | set(Cache.link_pic.keys()) | set(Cache.link_pic.values())
cartes |= set(ImageCreator.face_back_dict.keys())
noms |= cartes
noms |= {"fr_" + n for n in list(noms) if not n.startswith("fr_") and "/" not in n}
noms.discard("")

# HD : seulement les identites et les mechants (la scene de l'assistant), comme le jeu les demande.
identites = {cid for cid, p in CardsDB.papers.items()
             if getattr(p, "type", "") in ("Hero", "AlterEgo", "Alter-Ego", "Villain")}

resultat = {"image": {}, "vignette": {}, "hd": {}}
tous = sorted(noms)
for i, nom in enumerate(tous):
    resultat["image"][nom] = resoudre("image", nom, Cache.LoadImage)
    if "/" not in nom:
        resultat["vignette"][nom] = resoudre("vignette", nom, Cache.LoadVignette)
    if nom in identites:
        resultat["hd"][nom] = resoudre("hd", nom, Cache.LoadImageHD)
    if i % 2000 == 0:
        print(f"{i}/{len(tous)}", flush=True)

# LES CIBLES COUCHEES (plus larges que hautes), que `installer-images.py` sert
# depuis `pivotes/` : le moteur redresse en portrait toute image couchee. Oubliee
# jusqu'au 08/10/2026 : sans elle, TOUS les paysages partaient non redresses.
from PIL import Image
couchees = set()
for cible in {c for table in resultat.values() for c in table.values()}:
    if cible.startswith("generes/"):
        continue
    try:
        with Image.open(os.path.join("assets", cible)) as image:
            largeur, hauteur = image.size
    except Exception:
        continue
    if largeur > hauteur:
        couchees.add(cible)
resultat["_couchees"] = sorted(couchees)

with open(os.path.join(sortie, "resolution.json"), "w", encoding="utf-8") as f:
    json.dump(resultat, f, ensure_ascii=False)
gen = sum(1 for k, r in resultat.items() if k != "_couchees" for v in r.values() if v.startswith("generes/"))
print(f"noms : {len(tous)} ; vignettes : {len(resultat['vignette'])} ; hd : {len(resultat['hd'])} ; fabriques : {gen} ; couchees : {len(couchees)}")
