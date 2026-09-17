"""Le site et le jeu doivent afficher LA MEME mascotte au meme instant.

⚠ POURQUOI CE FICHIER EXISTE (17/09/2026). La rotation est calculee DEUX FOIS :
en Python pour le site (`site/narval.py`, page d'attente et favicon) et en
JavaScript pour le jeu (`public/js/prepare/narval.js`, ecran de preparation).
Les deux processus vivent sur deux sous-domaines et ne partagent rien.

Si l'une des deux listes gagne une mascotte que l'autre n'a pas, ou si les
durees s'ecartent, l'onglet et la page montrent deux narvals differents au meme
moment. Personne ne s'en apercevrait avant de le voir a l'ecran.

Ce test lit les deux fichiers, compare les listes, la duree, et rejoue la
formule sur deux ans pour verifier qu'elles ne divergent jamais.

Usage : python3 site/test_narval.py
"""
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JS = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "public", "js", "prepare", "narval.js")
STATIQUES = os.path.join(ICI, "static")
TEXTURES = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "assets", "textures")

sys.path.insert(0, ICI)
import narval  # noqa: E402

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom
          + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


def liste_js() -> list:
    texte = open(JS, encoding="utf-8").read()
    brut = re.search(r"export const NARVALS = \[(.*?)\]", texte, re.S)
    return re.findall(r'"([^"]+)"', brut.group(1)) if brut else []


def heures_js() -> int:
    texte = open(JS, encoding="utf-8").read()
    trouve = re.search(r"export const HEURES = (\d+)", texte)
    return int(trouve.group(1)) if trouve else -1


print("La mascotte tourne pareil des deux cotes")

verifier("les deux listes sont identiques",
         list(narval.NARVALS) == liste_js(),
         "python=%s js=%s" % (list(narval.NARVALS), liste_js()))
verifier("la duree est la meme", narval.HEURES == heures_js(),
         "python=%s js=%s" % (narval.HEURES, heures_js()))

# ⚠ LA FORMULE, PAS SEULEMENT LES CONSTANTES. Deux listes identiques avec deux
# calculs differents donneraient quand meme deux mascottes.
noms = liste_js()
divergences = []
if noms and narval.HEURES == heures_js():
    pas = narval.HEURES * 3600
    for i in range(0, 365 * 2 * 24 * 3600, pas // 2):      # deux ans, deux points par tranche
        attendu_py = narval.narval(i)
        # Le JS fait Math.floor(ms / 1000 / (HEURES*3600)) : meme division.
        attendu_js = noms[(i // pas) % len(noms)]
        if attendu_py != attendu_js:
            divergences.append((i, attendu_py, attendu_js))
            break
verifier("la formule donne le meme resultat sur deux ans", not divergences,
         str(divergences[:1]))

# Chaque mascotte declaree doit exister des DEUX cotes, sinon elle s'affiche en
# image cassee pendant trois heures.
manquantes = []
for nom in narval.NARVALS:
    fichier = "narwhal-%s.png" % nom
    if not os.path.isfile(os.path.join(STATIQUES, fichier)):
        manquantes.append("site/static/" + fichier)
    if not os.path.isfile(os.path.join(TEXTURES, fichier)):
        manquantes.append("assets/textures/" + fichier)
verifier("chaque mascotte existe des deux cotes", not manquantes, ", ".join(manquantes))

# ⚠ ET ELLE TOURNE VRAIMENT. Une liste d'un seul element, ou une duree a zero,
# passerait tous les cas ci-dessus sans rien faire tourner.
vus = {narval.narval(i * narval.HEURES * 3600) for i in range(len(narval.NARVALS) * 2)}
verifier("toutes les mascottes passent a l'antenne",
         vus == set(narval.NARVALS), "vues : %s" % sorted(vus))

print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
