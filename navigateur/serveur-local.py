#!/usr/bin/env python3
"""Serveur statique d'ESSAI pour navigateur/dist : memes en-tetes que ceux a poser sur le vrai hebergeur
(COOP/COEP) et resolution des scans comme le fait le moteur (assets/pics-fr, pics, textures, cache ; .webp .jpg .png).

    python3 navigateur/serveur-local.py [port]     puis ouvrir http://localhost:<port>/navigateur.html
"""
import http.server, socketserver, sys, os, mimetypes, io
from PIL import Image, ImageOps
RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
ASSETS = os.environ.get("ASSETS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Fusion", "marvel-lcg-src", "assets"))
DOSSIERS = ("pics-fr", "pics", "textures", "cache", "vignettes")

def trouver_scan(nom):
    for d in DOSSIERS:
        for ext in (".webp", ".jpg", ".png", ".svg", ""):
            p = os.path.join(ASSETS, d, nom + ext)
            if os.path.isfile(p):
                return p
    return None

CACHE_IMG = {}

def servir_scan(f):
    """Comme le moteur (engine/file/cache.py -> ImageCreator.TryRotateImage) : EXIF applique, puis toute
    image plus large que haute est tournee de 90 degres. Le plateau la remet a plat par CSS : sans cette
    rotation, les manigances et cartes de statut s'affichent couchees."""
    if f in CACHE_IMG:
        return CACHE_IMG[f]
    im = ImageOps.exif_transpose(Image.open(f))
    if im.width > im.height:
        im = im.rotate(90, expand=True)
        if f.lower().endswith((".jpg", ".jpeg")) and im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        buf = io.BytesIO(); im.save(buf, "WEBP" if f.endswith(".webp") else "PNG" if f.endswith(".png") else "JPEG", quality=90)
        data = buf.getvalue()
    else:
        data = open(f, "rb").read()
    CACHE_IMG[f] = data
    return data

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=RACINE, **k)
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def log_message(self, *a): pass
    def do_GET(self):
        chemin = self.path.split("?")[0]
        local = self.translate_path(chemin)
        if chemin.startswith("/scan/") or (not os.path.exists(local) and "." not in os.path.basename(chemin)):
            f = trouver_scan(os.path.basename(chemin))
            if f:
                data = servir_scan(f)
                self.send_response(200); self.send_header("Content-Type", mimetypes.guess_type(f)[0] or "image/jpeg")
                self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        return super().do_GET()
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".mjs": "text/javascript", ".wasm": "application/wasm", ".js": "text/javascript", ".json": "application/json", ".webp": "image/webp"}

socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("0.0.0.0", int(sys.argv[1]) if len(sys.argv) > 1 else 8770), H) as s:
    s.serve_forever()
