#!/usr/bin/env python3
"""Telecharge la galerie MC/DC 2026 (https://www.mcdc.fun/2026-card-gallery).

Relancable : un fichier deja present et non vide n'est pas retelecharge.
Ecrit dans sources/galerie/<section>/<nom decode> (dossier ignore par git)
et regenere sources/galerie/inventaire.json (section, nom, url, octets).
Usage : python3 telecharger-galerie.py
"""
import json, os, re, sys, urllib.parse, urllib.request

URL = "https://www.mcdc.fun/2026-card-gallery"
UA = {"User-Agent": "Mozilla/5.0"}
SECTIONS = ["basic", "aggression", "justice", "leadership", "protection", "campaign-challenge", "other"]
RE_IMG = re.compile(r'(?:data-src|src|data-image)=["\']((?:https?:)?//images\.squarespace-cdn\.com[^"\']+)')
ICI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(ICI, "sources", "galerie")


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def main():
    html = get(URL).decode("utf-8", "replace")
    bornes = []
    for s in SECTIONS:
        m = re.search(r'id="%s"' % re.escape(s), html)
        if not m:
            sys.exit("section introuvable : " + s)
        bornes.append((m.start(), s))
    bornes.sort()
    inventaire, vus = [], set()
    for m in RE_IMG.finditer(html):
        url = m.group(1)
        if url.startswith("//"):
            url = "https:" + url
        url = url.split("?")[0]
        if url in vus:
            continue
        vus.add(url)
        sec = "campagne-punisher"
        for pos, s in bornes:
            if m.start() >= pos:
                sec = s
        nom = urllib.parse.unquote_plus(url.rsplit("/", 1)[1])
        inventaire.append({"section": sec, "nom": nom, "url": url})
    print(len(inventaire), "images uniques")
    for it in inventaire:
        d = os.path.join(DEST, it["section"])
        os.makedirs(d, exist_ok=True)
        f = os.path.join(d, it["nom"])
        if not (os.path.isfile(f) and os.path.getsize(f) > 0):
            with open(f, "wb") as o:
                o.write(get(it["url"]))
        it["octets"] = os.path.getsize(f)
    with open(os.path.join(DEST, "inventaire.json"), "w", encoding="utf-8") as o:
        json.dump(inventaire, o, ensure_ascii=False, indent=1)
    print("ok :", sum(1 for i in inventaire if i["octets"] > 0), "fichiers dans", DEST)


main()
