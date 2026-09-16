"""Un module importe en tete ne se reimporte JAMAIS dans une fonction.

    python3 site/test_imports_locaux.py

⚠ POURQUOI, ET CA A CASSE LE SITE. Un `import urllib.parse` pose dans une
BRANCHE de `do_GET` fait de `urllib` une variable LOCALE a toute la methode.
Les autres branches, qui ne l'importent pas, n'ont alors plus rien : Python
leve `UnboundLocalError: local variable 'urllib' referenced before assignment`,
le gestionnaire meurt, la connexion se ferme, et Caddy affiche un 502.

Mesure en production le 16/09/2026 : `/regarder?joueur=...` repondait 502 a
chaque appel depuis sa livraison la veille, alors que le fichier importe
`urllib.parse` des sa ligne 40. Le journal de l'orchestrateur le disait mot
pour mot ; la page, elle, ne disait que « Cette page ne fonctionne pas ».

⚠ RIEN NE LE SIGNALE A LA LECTURE. Le code de la branche fautive est correct
vu seul, et les branches qui portent l'import marchent. Seul le chemin
d'execution qui saute l'import casse, et il faut donc une gate statique.
"""

import ast
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER = os.path.join(ICI, 'orchestrateur.py')

echecs = []


def racine_du_module(noeud):
    """Les noms de modules ancres par cet import, racine seule.

    `import urllib.parse` lie le nom `urllib`, pas `urllib.parse` : c'est la
    racine qui devient locale, donc la racine qu'on compare.
    """
    noms = set()
    if isinstance(noeud, ast.Import):
        for alias in noeud.names:
            noms.add((alias.asname or alias.name).split('.')[0])
    return noms


def main():
    arbre = ast.parse(open(FICHIER, encoding='utf-8').read(), FICHIER)

    # Ce qui est importe AU NIVEAU DU MODULE : disponible partout, sans rien.
    en_tete = set()
    for noeud in arbre.body:
        en_tete |= racine_du_module(noeud)

    print(f"Modules importes en tete : {len(en_tete)}")

    for fonction in ast.walk(arbre):
        if not isinstance(fonction, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for noeud in ast.walk(fonction):
            if not isinstance(noeud, ast.Import):
                continue
            for nom in racine_du_module(noeud) & en_tete:
                echecs.append(
                    f"{FICHIER}:{noeud.lineno} : `import {nom}...` dans "
                    f"{fonction.name}() alors que le module est deja importe "
                    f"en tete. Il devient LOCAL a toute la fonction, et toute "
                    f"branche qui ne passe pas par cet import plante en "
                    f"UnboundLocalError.")

    if echecs:
        print(f"\nECHEC : {len(echecs)} import(s) local(aux) masquant(s).")
        for e in echecs:
            print("  - " + e)
        return 1
    print("  ok   aucun import local ne masque un module de l'en-tete")
    return 0


if __name__ == '__main__':
    sys.exit(main())
