"""Une cible inconnue dans un script de carte, ca ne doit pas arriver.

    python3 tools/verifier_cibles.py            (depuis Fusion/marvel-lcg-src)

POURQUOI CET OUTIL EXISTE
-------------------------
`Select.From(target)` (src/game/selector/factory.py) ne sait pas dire « je ne
connais pas cette cible ». Un nom qu'il ne reconnait pas devient un
`SelectorTarget` sans fonction de cibles, et `SelectorTarget.GetAllTarget`
retombe EN SILENCE sur la zone par defaut, c'est-a-dire les cartes en jeu.
Le 12/10/2026, Swarmed by Rats (hs018/hs019) visait "HandCard" au lieu de
"YourHandCards" : son cout « defausse deux cartes de ta main » etait propose
main vide et se payait avec des cartes de la table (corrige dans b9b134f8).

Le repli reste tel quel en partie (pas de plantage devant les joueurs) : c'est
CETTE PORTE qui interdit qu'un nom inconnu soit commite.

CE QUE FAIT L'OUTIL
-------------------
1. Il deduit du code du moteur la liste des cibles RECONNUES, sans en garder
   de copie : les cles de `TARGET_MAP_FUNC` (selector_target_helper.py) et les
   noms traites a part dans `Select.From` (`target == "..."`).
2. Il deduit les fonctions dont un parametre `target` finit dans
   `Select.From` / `SetTarget` (CostFunc.*, AbilityFactory.*, SetTarget...),
   jusqu'au point fixe.
3. Il parcourt tous les scripts src/cards/pack/**/*.py et signale chaque
   CHAINE LITTERALE passee a l'un de ces parametres qui n'est pas reconnue,
   avec fichier:ligne. Sortie 1 s'il y en a.

Seules les chaines litterales sont jugees : une variable, une liste de
cartes, un CardFinder ou une fonction ne peuvent pas etre « inconnus ».

CALIBRAGE (§9 de PROCESSUS-CARTE)
---------------------------------
Vue rouge le 12/10/2026 sur le contenu de hs019.py d'avant b9b134f8
(« "HandCard" ») : ECHEC, sortie 1. Verte sur l'arbre corrige.
"""
from __future__ import annotations

import ast
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, "src")
FABRIQUE = os.path.join(SRC, "game", "selector", "factory.py")
AIDE = os.path.join(SRC, "game", "selector", "selector_target_helper.py")
CARTES = os.path.join(SRC, "cards", "pack")

# Fonctions « puits » : un `target` qui leur est passe est une cible de selection.
PUITS = {"From", "SetTarget", "SetTarget2", "SetTarget3"}


def _lire(chemin: str) -> ast.AST:
    with open(chemin, encoding="utf-8") as f:
        return ast.parse(f.read(), chemin)


def cibles_reconnues() -> set[str]:
    reconnues: set[str] = set()
    for noeud in ast.walk(_lire(AIDE)):
        if isinstance(noeud, (ast.Assign, ast.AnnAssign)):
            cibles = noeud.targets if isinstance(noeud, ast.Assign) else [noeud.target]
            if any(isinstance(c, ast.Name) and c.id == "TARGET_MAP_FUNC" for c in cibles):
                if isinstance(noeud.value, ast.Dict):
                    for cle in noeud.value.keys:
                        if isinstance(cle, ast.Constant) and isinstance(cle.value, str):
                            reconnues.add(cle.value)
    for noeud in ast.walk(_lire(FABRIQUE)):
        if isinstance(noeud, ast.FunctionDef) and noeud.name == "From":
            for n in ast.walk(noeud):
                if (isinstance(n, ast.Compare) and isinstance(n.left, ast.Name) and n.left.id == "target"
                        and len(n.ops) == 1 and isinstance(n.ops[0], ast.Eq)
                        and isinstance(n.comparators[0], ast.Constant) and isinstance(n.comparators[0].value, str)):
                    reconnues.add(n.comparators[0].value)
    if not reconnues:
        raise SystemExit("ECHEC : aucune cible reconnue lue dans le moteur (structure changee ?)")
    return reconnues


def _nom_appele(appel: ast.Call) -> str | None:
    if isinstance(appel.func, ast.Attribute):
        return appel.func.attr
    if isinstance(appel.func, ast.Name):
        return appel.func.id
    return None


def _indices(appel: ast.Call, positions: dict[str, set[int]]) -> set[int]:
    nom = _nom_appele(appel)
    if nom in PUITS:
        return {0}
    indices: set[int] = set()
    for cle, pos in positions.items():
        if _correspond(appel, cle):
            indices |= pos
    return indices


def _param_target_transmis(appel: ast.Call, positions: dict[str, set[int]]) -> bool:
    """L'appel transmet-il le nom `target` a un parametre-cible connu ?"""
    indices = _indices(appel, positions)
    if not indices and _nom_appele(appel) not in PUITS:
        return False
    for i, arg in enumerate(appel.args):
        if i in indices and isinstance(arg, ast.Name) and arg.id == "target":
            return True
    return any(k.arg == "target" and isinstance(k.value, ast.Name) and k.value.id == "target" for k in appel.keywords)


def _qualifie(appel: ast.Call) -> str | None:
    """« CostFunc.Discard(...) » -> « CostFunc.Discard » ; « x.SetTarget(...) » -> « .SetTarget » ;
    « Foo(...) » -> « Foo »."""
    if isinstance(appel.func, ast.Attribute):
        if isinstance(appel.func.value, ast.Name):
            return f"{appel.func.value.id}.{appel.func.attr}"
        return f".{appel.func.attr}"
    if isinstance(appel.func, ast.Name):
        return appel.func.id
    return None


def _correspond(appel: ast.Call, cle: str) -> bool:
    """Une cle « Classe » (constructeur imbrique, ex. « CostFunc.Discard ») ne
    correspond qu'a un appel qualifie par sa classe englobante ; une cle de
    methode (« .SetTarget2 ») correspond a tout appel `x.SetTarget2(...)`."""
    q = _qualifie(appel)
    if q is None:
        return False
    if cle.startswith("."):
        return q.endswith(cle)
    return q == cle


def fonctions_a_cible() -> dict[str, set[int]]:
    """Cle d'appel -> positions (hors self/cls) de son parametre `target`.

    Cles : « CostFunc.Discard » (constructeur d'une classe imbriquee),
    « Classe » (constructeur d'une classe de premier niveau), « .Methode »
    (methode), « fonction » (fonction libre).
    """
    candidates: list[tuple[str, int, ast.FunctionDef]] = []

    def visiter_classe(classe: ast.ClassDef, englobante: str | None) -> None:
        for f in classe.body:
            if isinstance(f, ast.ClassDef):
                visiter_classe(f, classe.name)
            elif isinstance(f, ast.FunctionDef):
                params = [a.arg for a in f.args.args]
                if params and params[0] in ("self", "cls"):
                    params = params[1:]
                if "target" not in params:
                    continue
                if f.name == "__init__":
                    cle = f"{englobante}.{classe.name}" if englobante else classe.name
                else:
                    cle = f".{f.name}"
                candidates.append((cle, params.index("target"), f))

    for dossier, _, fichiers in os.walk(os.path.join(SRC, "game")):
        for nom in fichiers:
            if not nom.endswith(".py"):
                continue
            arbre = _lire(os.path.join(dossier, nom))
            for noeud in arbre.body:
                if isinstance(noeud, ast.ClassDef):
                    visiter_classe(noeud, None)
                elif isinstance(noeud, ast.FunctionDef):
                    params = [a.arg for a in noeud.args.args]
                    if "target" in params:
                        candidates.append((noeud.name, params.index("target"), noeud))
    positions: dict[str, set[int]] = {}
    change = True
    while change:
        change = False
        for cle, indice, f in candidates:
            if indice in positions.get(cle, set()):
                continue
            if any(isinstance(n, ast.Call) and _param_target_transmis(n, positions) for n in ast.walk(f)):
                positions.setdefault(cle, set()).add(indice)
                change = True
    return positions


def chaines_cibles(chemin: str, positions: dict[str, set[int]]):
    for appel in ast.walk(_lire(chemin)):
        if not isinstance(appel, ast.Call):
            continue
        indices = _indices(appel, positions)
        if not indices and _nom_appele(appel) not in PUITS:
            continue
        valeurs = [a for i, a in enumerate(appel.args) if i in indices]
        valeurs += [k.value for k in appel.keywords if k.arg == "target"]
        for v in valeurs:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                yield v.lineno, _qualifie(appel) or "?", v.value


def verifier(chemins: list[str] | None = None) -> list[tuple[str, int, str, str]]:
    reconnues = cibles_reconnues()
    positions = fonctions_a_cible()
    if chemins is None:
        chemins = []
        for dossier, _, fichiers in os.walk(CARTES):
            chemins += [os.path.join(dossier, f) for f in fichiers if f.endswith(".py")]
    inconnues = []
    for chemin in sorted(chemins):
        for ligne, nom, valeur in chaines_cibles(chemin, positions):
            if valeur not in reconnues:
                inconnues.append((os.path.relpath(chemin, RACINE), ligne, nom, valeur))
    return inconnues


def main() -> None:
    inconnues = verifier(sys.argv[1:] or None)
    if inconnues:
        print(f"ECHEC : {len(inconnues)} cible(s) inconnue(s) du moteur (repli silencieux sur les cartes en jeu) :")
        for chemin, ligne, nom, valeur in inconnues:
            print(f"  {chemin}:{ligne}  {nom}(... {valeur!r} ...)")
        sys.exit(1)
    print("OK : toutes les cibles nommees dans les scripts de cartes sont connues du moteur.")


if __name__ == "__main__":
    main()
