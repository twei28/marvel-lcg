"""Chaque effet d'un choix « soit... soit... » porte un libellé propre.

Signalé en jeu le 10/10/2026 (Proxima Midnight 21092, Tower Defense) : deux
options d'une même carte s'affichaient comme deux vignettes identiques, et rien
ne disait laquelle faisait quoi. Le plateau nomme maintenant chaque option par
son libellé ; ce test garantit que chaque script EN DONNE un.

Balaye tous les `ChooseAbilities(effect, opt1, opt2, ...)` de src/cards à
deux options ou plus et exige pour chaque option un libellé non vide, et des
libellés distincts entre eux. Lancement : python3 tools/test_libelles_choix.py
"""
import ast
import os
import sys

RACINE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'cards')
CHAINAGES = {'SetTarget', 'SetLabel', 'SetCondition', 'SetConditions', 'SetUI', 'SetRepeat', 'SetSearch',
             'SetCost', 'SetCostFunc', 'SetHasNoTargetEffect', 'SetFuncName'}


def nom_appel(n: ast.Call) -> str:
    f = n.func
    return f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else '')


def sans_chainage(n: ast.AST) -> ast.AST:
    while (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
           and n.func.attr in CHAINAGES and isinstance(n.func.value, ast.Call)):
        n = n.func.value
    return n


def texte(n: ast.AST | None, params: dict[str, ast.AST]) -> str | None:
    """Le libellé lisible, '' s'il est vide, None si on ne sait pas le lire."""
    if n is None:
        return None
    if isinstance(n, ast.Constant) and isinstance(n.value, str):
        return n.value.strip()
    if isinstance(n, ast.JoinedStr):
        return ast.unparse(n)
    if isinstance(n, ast.Name) and n.id in params:
        return texte(params[n.id], {})
    return None


class Analyse:
    def __init__(self) -> None:
        self.fonctions: dict[str, ast.FunctionDef] = {}
        self.fautes: list[str] = []
        self.vus = 0
        self.deja: set[tuple[str, int]] = set()

    def libelle(self, n: ast.AST, locales: dict[str, ast.AST], profondeur: int = 0) -> str | None:
        n = sans_chainage(n)
        if isinstance(n, ast.Name) and n.id in locales and profondeur < 4:
            return self.libelle(locales[n.id], locales, profondeur + 1)
        if not isinstance(n, ast.Call):
            return None
        nom = nom_appel(n)
        mots = {k.arg: k.value for k in n.keywords if k.arg}
        if nom == 'ForChoiceAbilityWithCost':
            arg = mots.get('name', n.args[1] if len(n.args) > 1 else None)
            if arg is None or (isinstance(arg, ast.Constant) and arg.value is None):
                return 'Spend ' + ast.unparse(n.args[0]) if n.args else 'Spend'
            return texte(arg, {})
        if nom.startswith('ForChoiceAbility'):
            return texte(mots.get('name', n.args[0] if n.args else None), {})
        if nom == 'Otherwise':
            return 'Otherwise'
        defn = self.fonctions.get(nom)
        if defn is not None and profondeur < 4:
            params = {a.arg: v for a, v in zip(defn.args.args, n.args)}
            params.update(mots)
            for r in ast.walk(defn):
                if isinstance(r, ast.Return) and r.value is not None:
                    interne = sans_chainage(r.value)
                    if isinstance(interne, ast.Call) and nom_appel(interne).startswith('ForChoiceAbility'):
                        cle = 1 if nom_appel(interne) == 'ForChoiceAbilityWithCost' else 0
                        a = interne.args[cle] if len(interne.args) > cle else None
                        return texte(a, params)
        return None

    def fichier(self, chemin: str, arbre: ast.Module) -> None:
        for fonction in [n for n in ast.walk(arbre) if isinstance(n, (ast.FunctionDef, ast.Lambda))]:
            locales: dict[str, ast.AST] = {}
            corps = fonction.body if isinstance(fonction, ast.FunctionDef) else []
            for n in ast.walk(ast.Module(body=corps, type_ignores=[])) if corps else []:
                if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                    locales[n.targets[0].id] = n.value
            for n in ast.walk(fonction) if isinstance(fonction, ast.FunctionDef) else []:
                if not (isinstance(n, ast.Call) and nom_appel(n) == 'ChooseAbilities'):
                    continue
                options = n.args[1:]
                if len(options) < 2 or any(isinstance(o, ast.Starred) for o in options):
                    continue
                if (chemin, n.lineno) in self.deja:
                    continue
                self.deja.add((chemin, n.lineno))
                self.vus += 1
                libelles = [self.libelle(o, locales) for o in options]
                lieu = f'{os.path.relpath(chemin, RACINE)}:{n.lineno}'
                if any(l == '' for l in libelles):
                    self.fautes.append(f'{lieu} : une option sans libellé {libelles}')
                connus = [l for l in libelles if l]
                if len(connus) != len(set(connus)):
                    self.fautes.append(f'{lieu} : deux options au même libellé {libelles}')


def main() -> int:
    analyse = Analyse()
    arbres: list[tuple[str, ast.Module]] = []
    for racine, _, fichiers in os.walk(RACINE):
        for f in sorted(fichiers):
            if f.endswith('.py'):
                chemin = os.path.join(racine, f)
                arbres.append((chemin, ast.parse(open(chemin, encoding='utf-8').read(), chemin)))
    for _, arbre in arbres:
        for n in arbre.body:
            if isinstance(n, ast.FunctionDef):
                analyse.fonctions.setdefault(n.name, n)
    for chemin, arbre in arbres:
        analyse.fichier(chemin, arbre)
    for faute in analyse.fautes:
        print('ECHEC', faute)
    print(f'{analyse.vus} choix à plusieurs options lus, {len(analyse.fautes)} sans libellé distinct')
    return 1 if analyse.fautes else 0


if __name__ == '__main__':
    sys.exit(main())
