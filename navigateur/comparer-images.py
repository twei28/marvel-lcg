#!/usr/bin/env python3
"""Compare, adresse par adresse, ce que servent le jeu CLASSIQUE et play.<domaine>.

    python3 navigateur/comparer-images.py <resolution.json> <classique> <play> [--echantillon N]

    <classique> : un moteur classique, ex. http://127.0.0.1:2345 (cookie de version pose tout seul)
    <play>      : https://play.narwhalchampions.com

Les adresses : toutes celles de resolution.json (images, vignettes, HD), tous les sons, tous les SVG des
textures. Une image est « la meme » si les deux reponses sont 200 et que les images decodees ont la meme taille
et le meme contenu (ecart moyen faible apres reduction : le redressement des scans paysage est fait par deux
outils differents, donc les octets different). Tout le reste doit etre identique a l'octet.

⚠ Interroger TOUT le classique charge chaque image dans la memoire du moteur (Cache.cache) : sur le moteur de
jeu du poste, garder --echantillon. Sans echantillon, viser un moteur d'essai.
"""
import concurrent.futures as cf, hashlib, io, json, os, random, sys, urllib.parse, urllib.request, http.cookiejar
from PIL import Image

args = [a for a in sys.argv[1:] if not a.startswith("--")]
resolution_json, classique, play = args[0], args[1].rstrip("/"), args[2].rstrip("/")
echantillon = int(sys.argv[sys.argv.index("--echantillon") + 1]) if "--echantillon" in sys.argv else 0
assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Fusion", "marvel-lcg-src", "assets")

res = json.load(open(resolution_json, encoding="utf-8"))
adresses = []
for nom in res["image"]:
    adresses.append("/" + nom)
for nom in res["vignette"]:
    adresses.append("/vignette/" + nom)
for nom in res["hd"]:
    adresses.append("/hd/" + nom)
for f in sorted(os.listdir(os.path.join(assets, "sounds"))):
    if f.lower().endswith((".wav", ".mp3")):
        adresses.append("/" + f)
for racine, _, fichiers in os.walk(os.path.join(assets, "textures")):
    for f in fichiers:
        if f.lower().endswith(".svg"):
            adresses.append("/" + f)
if echantillon:
    random.seed(7)
    adresses = random.sample(adresses, min(echantillon, len(adresses)))

jar = http.cookiejar.CookieJar()
ouvreur = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
try:
    ouvreur.open(classique + "/get_version", timeout=10).read()
except Exception:
    pass

def lire(url):
    try:
        r = ouvreur.open(urllib.request.Request(url, headers={"User-Agent": "comparer-images"}), timeout=30)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return 0, str(e).encode()

def empreinte_image(octets):
    try:
        im = Image.open(io.BytesIO(octets))
        im.load()
        petite = im.convert("RGB").resize((24, 24))
        return im.size, list(petite.getdata())
    except Exception:
        return None

def comparer(chemin):
    url = urllib.parse.quote(chemin)          # « /sets/1. Core Set » : espaces et signes encodes
    sc, bc = lire(classique + url)
    sp, bp = lire(play + url)
    if sc != 200 or sp != 200:
        return (chemin, f"statut classique {sc}, play {sp}") if sc != sp or sc != 200 else None
    if bc == bp:
        return None
    ec, ep = empreinte_image(bc), empreinte_image(bp)
    if ec is None or ep is None:
        return (chemin, "octets differents (pas une image decodable)")
    if ec[0] != ep[0]:
        return (chemin, f"tailles differentes : classique {ec[0]}, play {ep[0]}")
    ecart = sum(abs(a - b) for pa, pb in zip(ec[1], ep[1]) for a, b in zip(pa, pb)) / (24 * 24 * 3)
    return (chemin, f"contenu different (ecart moyen {ecart:.1f})") if ecart > 6 else None

ecarts = []
with cf.ThreadPoolExecutor(8) as ex:
    for i, r in enumerate(ex.map(comparer, adresses)):
        if r:
            ecarts.append(r)
        if i and i % 1000 == 0:
            print(f"{i}/{len(adresses)}, ecarts : {len(ecarts)}", flush=True)
print(f"ADRESSES : {len(adresses)} ; ECARTS : {len(ecarts)}")
for chemin, raison in ecarts:
    print(f"  {chemin} : {raison}")
sys.exit(1 if ecarts else 0)
