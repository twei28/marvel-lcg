"""Test rapide de outils/uniformiser-scans.py, en dossier temporaire.

Verifie les trois proprietes dont depend deployer.ps1 (audit E, point 4) :

  1. Idempotence : apres --sauvegarde puis --appliquer, une 2e passe ne
     trouve plus rien a traiter (elle ne re-degraderait pas une image deja
     reduite en repartant de son original sauvegarde).
  2. Refus si la sauvegarde d'un fichier a traiter manque, meme quand la
     sauvegarde existe deja pour d'AUTRES fichiers en nombre suffisant
     (regression du bug corrige le 06/09/2026 : un comptage global laissait
     passer un nouveau pack non sauvegarde).
  3. Aucune degradation : l'image reduite deux fois (300 puis 615, ou
     appliquee deux fois de suite) donne la meme taille finale, jamais plus
     petite que la cible faute de repartir de l'original.

Usage : python3 outils/test_uniformiser_scans.py
"""
import importlib.util
import os
import shutil
import sys
import tempfile

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom
          + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


def charger_module():
    """Import par chemin : le nom de fichier a un tiret, pas un `import` normal."""
    chemin = os.path.join(ICI, "uniformiser-scans.py")
    spec = importlib.util.spec_from_file_location("uniformiser_scans", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def image(chemin, largeur, hauteur):
    Image.new("RGB", (largeur, hauteur), color=(120, 40, 200)).save(chemin, "JPEG", quality=90)


def preparer(dossier):
    pics = os.path.join(dossier, "pics")
    sauvegarde = os.path.join(dossier, "sauvegarde")
    os.makedirs(pics)
    # Une grande (a reduire) et une deja a la bonne taille (a laisser).
    image(os.path.join(pics, "grande.jpg"), 1500, 2150)
    image(os.path.join(pics, "deja_ok.jpg"), 615, 880)
    return pics, sauvegarde


with tempfile.TemporaryDirectory(prefix="test-uniformiser-") as dossier:
    m = charger_module()
    m.PICS, m.SAUVEGARDE = preparer(dossier)

    # --- 1. a_traiter() ne retient que ce qui depasse REELLEMENT la cible ---
    liste = m.a_traiter()
    noms = sorted(os.path.basename(c) for c, _, _ in liste)
    verifier("a_traiter() ne retient que l'image trop grande",
              noms == ["grande.jpg"], str(noms))

    # --- 2. Refus fichier par fichier, meme avec un gros historique --------
    os.makedirs(m.SAUVEGARDE)
    for i in range(50):
        image(os.path.join(m.SAUVEGARDE, f"ancien_{i}.jpg"), 1500, 2150)
    try:
        m.appliquer()
        verifier("refus si l'original de grande.jpg n'est pas sauvegarde",
                  False, "aucune exception levee")
    except SystemExit:
        verifier("refus si l'original de grande.jpg n'est pas sauvegarde", True)
    verifier("grande.jpg n'a pas ete touchee par le refus",
              Image.open(os.path.join(m.PICS, "grande.jpg")).size == (1500, 2150))

    # --- 3. Sauvegarde puis application : dimension cible correcte ---------
    m.sauvegarder()
    verifier("l'original de grande.jpg est sauvegarde",
              os.path.exists(os.path.join(m.SAUVEGARDE, "grande.jpg")))
    m.appliquer()
    with Image.open(os.path.join(m.PICS, "grande.jpg")) as im:
        taille_1 = im.size
    verifier("grande.jpg reduite au petit cote cible",
              min(taille_1) == m.PETIT_COTE, str(taille_1))

    # --- 4. Idempotence : 2e et 3e passes sont des no-op ---------------------
    liste_2 = m.a_traiter()
    verifier("plus rien a traiter juste apres --appliquer", liste_2 == [], str(liste_2))

    m.appliquer()  # ne doit rien faire (liste vide -> return immediat)
    with Image.open(os.path.join(m.PICS, "grande.jpg")) as im:
        taille_2 = im.size
    verifier("une 2e application ne change pas la taille (no-op)",
              taille_2 == taille_1, f"{taille_1} -> {taille_2}")

    m.appliquer()  # 3e passe, meme verification
    with Image.open(os.path.join(m.PICS, "grande.jpg")) as im:
        taille_3 = im.size
    verifier("une 3e application ne change toujours rien (no-op)",
              taille_3 == taille_1, f"{taille_1} -> {taille_3}")

    # --- 5. L'image deja a la bonne taille n'a jamais ete touchee ----------
    verifier("deja_ok.jpg n'a jamais ete reecrite",
              Image.open(os.path.join(m.PICS, "deja_ok.jpg")).size == (615, 880))

print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
