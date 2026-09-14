"""La gate : tout import ecrit dans un script de carte doit exister.

    python3 outils/test_gate_imports_cartes.py

⚠ POURQUOI CETTE GATE EXISTE. `61004` "Big Mistake" portait, DANS une fonction,
`from game.element.attack_property import AttackProperty` : un module qui
n'existe pas (la classe vit dans `game/card/face/attribute/can_attack.py`, et
`from . import *` en tete de fichier l'apporte deja).

⚠ ET L'IMPORT ETAIT DANS UNE BRANCHE. Il ne s'executait que si le joueur
choisissait de payer une preuve. La carte marchait donc parfaitement sans la
preuve, et ne faisait RIEN avec : le moteur avale l'exception, la carte part a
la defausse, les degats ne sont jamais infliges. Rapporte en jeu le 14/09/2026 :
« j'ai paye une preuve et il n'a meme pas fait de degats du tout, la carte est
partie dans le vide ». Aucune erreur visible, aucun test rouge, un coup perdu.

⚠ ET C'EST PRECISEMENT CE QU'UN IMPORT EN TETE DE FICHIER N'AURAIT PAS FAIT :
il aurait casse au chargement du pack, donc tout de suite et pour tout le monde.
Un import enterre dans une branche rare est invisible jusqu'a ce que quelqu'un
emprunte cette branche, en partie, un an plus tard.

CE QUE LA GATE VERIFIE : chaque `import X` et `from X import ...` ecrit sous
`src/cards/`, A N'IMPORTE QUELLE PROFONDEUR (module, fonction, branche), designe
un module qui existe vraiment - dans le moteur, dans la bibliotheque standard,
ou dans les paquets tiers connus.

⚠ RESOLUTION PAR LE DISQUE, PAS PAR `importlib`. Importer pour verifier
executerait les `__init__` du moteur et ses imports en cascade, avec leurs
effets de bord, pour une question a laquelle l'arborescence repond seule.
"""

import ast
import io
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'src')
CARTES = os.path.join(SRC, 'cards')

# Les paquets tiers que le moteur embarque. La bibliotheque standard, elle, est
# lue depuis l'interpreteur : la lister a la main la ferait derailler a chaque
# version de Python.
TIERS = {'PIL', 'aiohttp', 'yaml', 'numpy', 'requests', 'websockets', 'cryptography'}


def modules_importes(chemin: str):
    """Chaque module cite par un import de ce fichier, avec sa ligne.

    Les imports RELATIFS (`from . import *`) sont ignores : ils se resolvent par
    l'arborescence du paquet, et une erreur y casse le chargement du pack tout
    entier, donc immediatement et pour tout le monde. Ce ne sont pas eux qui
    peuvent se cacher dans une branche.
    """
    with io.open(chemin, encoding='utf-8') as f:
        arbre = ast.parse(f.read(), filename=chemin)
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            for alias in noeud.names:
                yield alias.name, noeud.lineno
        elif isinstance(noeud, ast.ImportFrom):
            if noeud.level and noeud.level > 0:
                continue
            if noeud.module:
                yield noeud.module, noeud.lineno


def existe(module: str) -> bool:
    racine = module.split('.')[0]
    if racine in sys.stdlib_module_names or racine in TIERS:
        return True
    chemin = os.path.join(SRC, *module.split('.'))
    return os.path.isfile(chemin + '.py') or os.path.isfile(os.path.join(chemin, '__init__.py'))


def scripts_de_cartes():
    for dossier, _, fichiers in os.walk(CARTES):
        if '__pycache__' in dossier:
            continue
        for nom in sorted(fichiers):
            if nom.endswith('.py'):
                yield os.path.join(dossier, nom)


def main() -> int:
    # 1. LA LOGIQUE REFUSE BIEN UN MODULE ABSENT, ET ACCEPTE UN MODULE PRESENT.
    #    Une gate qui repond « OK » n'est une preuve que si on l'a vue echouer
    #    (PROCESSUS-CARTE.md, §9).
    assert existe('os'), 'la bibliotheque standard doit passer'
    assert existe('game.card.face.attribute.can_attack'), 'un module du moteur doit passer'
    assert existe('game.card.face'), 'un paquet du moteur doit passer'
    assert not existe('game.element.attack_property'), (
        "le module fantome de 61004 doit ETRE REFUSE ; s'il passe, la gate ne "
        "protege plus rien"
    )
    assert not existe('game.ce.module.na.jamais.existe')

    # 2. AUCUNE CARTE DU CATALOGUE NE PORTE PLUS LA FAUTE.
    fautes = []
    fichiers = 0
    imports = 0
    for chemin in scripts_de_cartes():
        fichiers += 1
        for module, ligne in modules_importes(chemin):
            imports += 1
            if not existe(module):
                fautes.append((os.path.relpath(chemin, RACINE), ligne, module))

    print(f"{fichiers} scripts de cartes, {imports} imports absolus verifies.")
    if fautes:
        print(f"\n❌ {len(fautes)} import(s) vers un module INEXISTANT :\n")
        for fichier, ligne, module in fautes:
            print(f"  {fichier}:{ligne}  ->  {module}")
        print(
            "\nUn import enterre dans une branche ne casse QUE cette branche, en "
            "partie, sans erreur visible. Corriger a la source."
        )
        return 1
    print("✅ Aucun import fantome.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
