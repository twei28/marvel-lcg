"""Verifie qu'une ecriture ratee ne detruit pas ce qui etait deja la.

Le module vise n'a que des imports standard : on le charge PAR SON CHEMIN, sans
amorcer le moteur ni importer un seul paquet du jeu. C'est tout l'interet de
l'avoir garde sans dependance.

Le cas qui compte est le troisieme : une panne au milieu de l'ecriture. C'est
exactement ce qui s'est produit le 10/8/2026 avec l'ancienne version, et c'est
le seul que l'ancien code ratait — les deux premiers passaient deja.

Usage: python3.10 tools/test_ecriture_atomique.py
"""
import importlib.util
import json
import os
import shutil
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEMIN = os.path.join(RACINE, "src", "engine", "ecriture_atomique.py")

spec = importlib.util.spec_from_file_location("ecriture_atomique", CHEMIN)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), str(detail)))


class NonSerialisable:
    """Casse json.dump APRES qu'il ait deja ecrit une partie de la sortie."""


bac = tempfile.mkdtemp(prefix="ecriture-atomique-")
try:
    cible = os.path.join(bac, "campagne.json")

    # 1. Ecriture nominale.
    module.ecrire_json(cible, {"nom": "Essai", "termines": ["s1"]})
    relu = json.load(open(cible, encoding="utf-8"))
    verifier("le fichier contient bien ce qu'on a ecrit", relu["nom"] == "Essai", relu)

    # 2. Remplacement d'un fichier existant.
    module.ecrire_json(cible, {"nom": "Essai", "termines": ["s1", "s2"]})
    relu = json.load(open(cible, encoding="utf-8"))
    verifier("un fichier existant est remplace", len(relu["termines"]) == 2, relu)

    # 3. LE cas : la serialisation casse en plein milieu.
    avant = open(cible, encoding="utf-8").read()
    try:
        module.ecrire_json(cible, {"nom": "Essai", "casse": NonSerialisable()})
        verifier("une ecriture impossible leve", False, "aucune exception")
    except TypeError:
        verifier("une ecriture impossible leve", True)

    apres = open(cible, encoding="utf-8").read()
    verifier("l'ancien contenu est INTACT apres l'echec", apres == avant,
             f"avant={len(avant)} octets, apres={len(apres)}")
    verifier("le fichier n'est pas vide", len(apres) > 0, len(apres))
    json.loads(apres)
    verifier("le fichier reste du JSON lisible", True)

    restes = [n for n in os.listdir(bac) if n.endswith(".tmp")]
    verifier("aucun temporaire ne survit a l'echec", not restes, restes)

    # 4. Le dossier de destination est cree au besoin.
    profond = os.path.join(bac, "pas", "encore", "la", "c.json")
    module.ecrire_json(profond, {"ok": True})
    verifier("le dossier manquant est cree", os.path.isfile(profond))
finally:
    shutil.rmtree(bac, ignore_errors=True)

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
