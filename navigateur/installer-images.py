#!/usr/bin/env python3
"""Installe SUR LE SERVEUR les images de play.<domaine>, telles que les resout le moteur classique.

    python3 installer-images.py <dossier de resoudre-images.py> /opt/narwhal-play-scans

Entree : `resolution.json` et `generes/`, produits par `navigateur/resoudre-images.py`.
Sortie : `<scans>/resolu/<route>/<nom>.<ext>`, route = image | vignette | hd.
  - un LIEN vers le scan deja copie sur le serveur, de preference sa version REDRESSEE (`pivotes/`, produite par
    preparer-scans.py : le moteur tourne en portrait toute image plus large que haute) ;
  - une COPIE pour ce que le moteur fabrique (carte dessinee, scan telecharge), venue de `generes/`.
Caddy n'a plus qu'a chercher `resolu/<route>/<dernier segment>.<ext>` : toute la chaine du moteur (dossiers,
extensions, liens, repli fr_, telechargement, carte dessinee) est deja dans les liens.

Le dossier est reconstruit a neuf (dans un dossier voisin, puis echange) : jamais d'etat a moitie fait en ligne.
"""
import json, os, shutil, sys

source, scans = sys.argv[1], sys.argv[2]
resolution = json.load(open(os.path.join(source, "resolution.json"), encoding="utf-8"))
# Les cibles COUCHEES (plus larges que hautes) : seules elles se servent redressees. Un fichier de pivotes/ pour
# une image debout est un reste d'une ancienne version (vu le 07/10/2026 : la vignette 50172, 1 px de trop).
couchees = set(resolution.pop("_couchees", []))
neuf = os.path.join(scans, "resolu.neuf")
shutil.rmtree(neuf, ignore_errors=True)
manquants = []
n = 0
for route, table in resolution.items():
    os.makedirs(os.path.join(neuf, route), exist_ok=True)
    for nom, cible in table.items():
        ext = os.path.splitext(cible)[1]
        lien = os.path.join(neuf, route, nom.replace("/", "__") + ext)
        if cible.startswith("generes/"):
            shutil.copyfile(os.path.join(source, cible), lien)
            n += 1
            continue
        for base in (("pivotes", "originaux") if cible in couchees else ("originaux",)):
            chemin = os.path.join(scans, base, cible)
            if os.path.isfile(chemin):
                os.symlink(chemin, lien)
                n += 1
                break
        else:
            manquants.append(f"{route}/{nom} -> {cible}")
ancien = os.path.join(scans, "resolu")
if os.path.isdir(ancien):
    shutil.rmtree(ancien + ".ancien", ignore_errors=True)
    os.rename(ancien, ancien + ".ancien")
os.rename(neuf, ancien)
shutil.rmtree(ancien + ".ancien", ignore_errors=True)
print(f"{n} images installees ; {len(manquants)} cibles absentes du serveur")
for m in manquants[:30]:
    print("  ABSENT", m)
