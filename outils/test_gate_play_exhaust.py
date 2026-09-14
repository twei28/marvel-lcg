"""La gate : une capacite de mise en jeu ne peut pas couter d'incliner sa carte.

    python3 outils/test_gate_play_exhaust.py

⚠ POURQUOI CETTE GATE EXISTE. `SetPlay()` baptise la capacite « Play » : le
moteur la presente comme la MISE EN JEU de la carte et l'evalue pendant qu'elle
est encore EN MAIN. Avec un cout `CostFunc.Exhaust("This")`, il faudrait
incliner une carte qui n'est pas sur la table : le cout n'a aucune cible et le
moteur repond « rien a depenser pour payer le cout ».

⚠ ET LA CARTE DEVIENT INJOUABLE POUR TOUJOURS, SANS QU'AUCUNE ERREUR NE SE VOIE.
Rien ne plante, aucun test ne rougit, la carte disparait simplement des options
proposees. C'est ce qui l'a rendue invisible : signale EN PARTIE le 14/09/2026
sur `62008` Burstein Process, et QUATRE autres cartes portaient la meme faute
(`61003`, `61008`, `61009`, `62018`), toutes injouables depuis toujours.

⚠ POURQUOI CE TEST NE MONTE PAS LE MOTEUR. Ses modules s'importent en cascade
depuis son point d'entree ; un import direct de `game.ability` part en import
circulaire. On verifie donc les trois maillons separement, et c'est leur
CONJONCTION qui fait la garantie :
  1. la logique de la gate refuse bien la combinaison, dans les deux sens ;
  2. les DEUX points d'entree (`SetPlay`, `SetCostFunc`) l'appellent, donc il
     n'existe aucun ordre d'ecriture qui passe entre les mailles ;
  3. aucune carte du catalogue ne porte plus la faute.
"""

import ast
import io
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'src')
ABILITY = os.path.join(SRC, 'game', 'ability', 'ability.py')
PACK = os.path.join(SRC, 'cards', 'pack')

echecs = []


def verifier(nom, obtenu, attendu):
    if obtenu == attendu:
        print(f"  ok   {nom}")
    else:
        print(f"  ECHEC {nom} : obtenu {obtenu!r}, attendu {attendu!r}")
        echecs.append(nom)


# --------------------------------------------------------------- 1. la gate --

def charger_la_gate():
    """Extrait `_refuser_play_avec_cout_sur_soi` de ability.py et la compile
    seule, sans rien importer du moteur."""
    arbre = ast.parse(io.open(ABILITY, encoding='utf-8').read())
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.FunctionDef) and noeud.name == '_refuser_play_avec_cout_sur_soi':
            module = ast.Module(body=[noeud], type_ignores=[])
            ast.fix_missing_locations(module)
            espace: dict = {}
            exec(compile(module, ABILITY, 'exec'), espace)
            return espace['_refuser_play_avec_cout_sur_soi']
    raise AssertionError("la gate a disparu de ability.py")


class FauxCout:
    def __init__(self, sur_soi):
        self.exige_cette_carte_en_jeu = sur_soi


class FausseCapacite:
    """Ce que la gate lit d'une capacite, et rien d'autre."""

    def __init__(self, noms, couts):
        self.func_names = set(noms)
        self.cost_funcs = list(couts)


def leve(gate, capacite) -> bool:
    try:
        gate(capacite)
        return False
    except AssertionError:
        return True


# ------------------------------------------- 2. les deux points d'entree --

def methodes_qui_appellent_la_gate():
    arbre = ast.parse(io.open(ABILITY, encoding='utf-8').read())
    trouvees = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.FunctionDef):
            continue
        for sous in ast.walk(noeud):
            if (isinstance(sous, ast.Call) and isinstance(sous.func, ast.Attribute)
                    and sous.func.attr == '_refuser_play_avec_cout_sur_soi'):
                trouvees.add(noeud.name)
    return trouvees


# ----------------------------------------------------- 3. le catalogue --

def cartes_fautives():
    def chaine(noeud):
        noms = []
        while isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute):
            noms.append(noeud.func.attr)
            noeud = noeud.func.value
        return noms

    def exhaust_this(noeud):
        for sous in ast.walk(noeud):
            if (isinstance(sous, ast.Call) and isinstance(sous.func, ast.Attribute)
                    and sous.func.attr == 'Exhaust'
                    and isinstance(sous.func.value, ast.Name) and sous.func.value.id == 'CostFunc'
                    and sous.args and isinstance(sous.args[0], ast.Constant)
                    and sous.args[0].value == 'This'):
                return True
        return False

    fautives, examinees = set(), 0
    for dossier, _, fichiers in os.walk(PACK):
        for nom in fichiers:
            if not nom.endswith('.py'):
                continue
            chemin = os.path.join(dossier, nom)
            examinees += 1
            try:
                arbre = ast.parse(io.open(chemin, encoding='utf-8').read())
            except SyntaxError:
                continue
            for noeud in ast.walk(arbre):
                if not isinstance(noeud, ast.Call) or 'SetPlay' not in chaine(noeud):
                    continue
                for appel in ast.walk(noeud):
                    if (isinstance(appel, ast.Call) and isinstance(appel.func, ast.Attribute)
                            and appel.func.attr == 'SetCostFunc'
                            and any(exhaust_this(a) for a in appel.args)):
                        fautives.add(os.path.relpath(chemin, PACK).replace(os.sep, '/'))
    return sorted(fautives), examinees


def main():
    gate = charger_la_gate()

    print("1. La gate refuse la combinaison")
    verifier("marquee Play, cout sur elle-meme",
             leve(gate, FausseCapacite({'Play'}, [FauxCout(True)])), True)
    verifier("le cout fautif noye parmi d'autres",
             leve(gate, FausseCapacite({'Play'}, [FauxCout(False), FauxCout(True)])), True)

    print("\n   et laisse passer ce qui est legitime")
    verifier("une action avec ce cout, SANS Play (le modele officiel)",
             leve(gate, FausseCapacite(set(), [FauxCout(True)])), False)
    verifier("Play avec un cout qui ne porte pas sur la carte",
             leve(gate, FausseCapacite({'Play'}, [FauxCout(False)])), False)
    verifier("Play sans aucun cout",
             leve(gate, FausseCapacite({'Play'}, [])), False)

    print("\n2. Les deux points d'entree l'appellent")
    # ⚠ SANS CECI LA GATE NE SERAIT QU'UNE FONCTION MORTE. Et il en faut DEUX :
    # `.SetPlay().SetCostFunc(...)` et `.SetCostFunc(...).SetPlay()` s'ecrivent
    # tous les deux, il ne doit exister aucun ordre qui passe entre les mailles.
    appelantes = methodes_qui_appellent_la_gate()
    verifier("SetPlay l'appelle", 'SetPlay' in appelantes, True)
    verifier("SetCostFunc l'appelle", 'SetCostFunc' in appelantes, True)

    print("\n3. Le catalogue est propre")
    fautives, examinees = cartes_fautives()
    print(f"   ({examinees} scripts de cartes examines)")
    verifier("aucune carte ne combine SetPlay et Exhaust(This)", fautives, [])

    print()
    if echecs:
        print(f"{len(echecs)} ECHEC(S) : " + ', '.join(echecs))
        return 1
    print("tout est vert")
    return 0


if __name__ == '__main__':
    sys.exit(main())
