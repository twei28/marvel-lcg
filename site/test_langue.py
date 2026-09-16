"""Toute phrase passee a `t()` a sa traduction anglaise.

    python3 site/test_langue.py
    python3 site/test_langue.py --manquantes   # les imprime, pretes a coller

⚠ POURQUOI. Le site etait ecrit en francais en dur, alors que le jeu est
bilingue depuis longtemps. La traduction s'est faite phrase par phrase : sans
un controle, l'anglais se serait degrade au premier ajout, exactement comme
c'est arrive au jeu le 15/09/2026 (« le SITE n'avait aucune gate, et 29 cles
s'affichaient en francais sur un ecran anglais »).

⚠ CE QU'IL NE PEUT PAS VOIR, et qu'il faut savoir : une phrase ecrite en dur
SANS passer par `t()` lui echappe. Il garantit que ce qui est traduit l'est
vraiment, pas que tout est traduit. Le compte ci-dessous sert a suivre
l'avancee du chantier.
"""
import ast
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import langue as lang  # noqa: E402

FICHIER = os.path.join(ICI, "orchestrateur.py")


def phrases_traduites(chemin: str) -> list:
    """Les litteraux passes a `lang.t(...)`, dans l'ordre du fichier."""
    arbre = ast.parse(open(chemin, encoding="utf-8").read(), chemin)
    trouvees = []
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        cible = noeud.func
        nom = ""
        if isinstance(cible, ast.Attribute):
            nom = cible.attr
        elif isinstance(cible, ast.Name):
            nom = cible.id
        if nom != "t" or not noeud.args:
            continue
        premier = noeud.args[0]
        # Les chaines ecrites sur plusieurs lignes sont deja recollees par
        # l'analyseur : un `ast.Constant` unique. Ce qui n'est PAS une
        # constante (une variable, un calcul) ne peut pas etre verifie ici.
        if isinstance(premier, ast.Constant) and isinstance(premier.value, str):
            trouvees.append(premier.value)
    return trouvees


def main() -> int:
    phrases = phrases_traduites(FICHIER)
    uniques = sorted(set(phrases))
    manquantes = [p for p in uniques if p not in lang.DICO_EN]

    print(f"phrases passees a t() : {len(uniques)} distinctes ({len(phrases)} appels)")
    print(f"traduites             : {len(uniques) - len(manquantes)}")

    if "--manquantes" in sys.argv[1:] and manquantes:
        print("\nA coller dans DICO_EN :")
        for p in manquantes:
            print(f'    {p!r}:\n        "",')

    if manquantes:
        print(f"\nECHEC : {len(manquantes)} phrase(s) sans traduction anglaise.")
        for p in manquantes[:10]:
            print(f"  - {p[:78]}")
        if len(manquantes) > 10:
            print(f"  ... et {len(manquantes) - 10} autres")
        return 1

    # ⚠ L'INVERSE COMPTE AUSSI : une cle qui ne sert plus alourdit le
    # dictionnaire et fait croire a une couverture qu'on n'a pas.
    orphelines = [c for c in lang.DICO_EN if c not in set(uniques)]
    if orphelines:
        print(f"\n⚠ {len(orphelines)} cle(s) du dictionnaire ne servent plus :")
        for c in orphelines[:5]:
            print(f"  - {c[:78]}")

    print("\n  ok   chaque phrase traduite a son anglais")
    return 0


if __name__ == "__main__":
    sys.exit(main())
