"""Les METHODES qu'un module de carte appelle existent-elles vraiment ?

    python3.10 tools/verifier_appels_modules.py <game_dir> <port> <pack> [pack ...]

⚠ `<game_dir>` doit etre ABSOLU (`"$PWD/.game-src"`). `main()` fait
`os.chdir(game_dir)` AVANT de lire `<game_dir>/launch.json` : avec un chemin
relatif il cherche `.game-src/launch.json` DEPUIS `.game-src` et sort sur
`FileNotFoundError`. Constate le 09/09/2026.

POURQUOI CET OUTIL EXISTE
-------------------------
« Ne jamais ecrire un appel d'API plausible » est une regle du projet, et elle a
ete violee deux fois dans le meme pack : `GainKeywordPermanently(...)` n'existe
pas, et pourtant dt073 et dt111 l'appelaient. Le code se chargeait, la carte se
construisait, `test_cards` etait vert, `test_generate_cards` aussi — parce que le
corps d'une fonction n'est execute qu'en PARTIE. Le joueur aurait vu un plantage.

`verifier_noms_modules.py` ne l'attrape pas, et sa doc le dit : il verifie les
NOMS (`Faces`, `Worlds`), pas les ATTRIBUTS (`Faces.GetAll`). C'est ce trou-la
que celui-ci bouche.

CE QU'IL FAIT
-------------
Il charge le moteur, puis relit chaque module en AST et releve tout appel de la
forme `X.methode(...)`. Pour chaque nom connu du namespace du pack (une classe,
un module), il verifie que l'attribut existe. Les appels sur une variable locale
(`this.DealDamage`) sont resolus quand le module dit son type par un `CastTo`.

CE QU'IL NE FAIT PAS
--------------------
Verifier la SIGNATURE (nombre et nom des parametres). Un appel existant mais mal
appele passe ici et tombera a la construction — ce que `test_cards` voit.
"""
import ast
import io
import os
import sys

# Les types que les modules manipulent, et ou les chercher. Un `CastTo(Ally)`
# dit le type d'une variable ; sans lui, on ne conclut rien.
def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    game_dir = os.path.expanduser(sys.argv[1])
    port = int(sys.argv[2])
    packs = sys.argv[3:]

    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ["RELEASE"] = "1"
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)
    # Le port du jeu est peut-etre pris par une partie en cours : on prend le
    # notre, comme le font les autres outils.
    import json
    cfg_path = os.path.join(game_dir, "launch.json")
    cfg = json.load(open(cfg_path))
    cfg["server_addresses"] = ["127.0.0.1:%d" % port]
    json.dump(cfg, open(cfg_path, "w"), indent=2)

    vrai_stdout = sys.stdout
    sys.stdout = sys.stderr = io.open("/tmp/verifier_appels_modules.log", "w", buffering=1)

    from engine import Engine
    Engine.Initialize()

    # ⚠ CORRECTIF DU 04/09/2026 : CETTE GATE ETAIT VIDE POUR 116 PACKS SUR 122.
    #
    # L'outil ne lisait QUE `src/cards/pack/<pack>/*.py`. Or un pack de heros
    # est range en `pack/<pack>/<set>/`, `pack/<pack>/<set>_nemesis/` : le seul
    # fichier au premier niveau est un `__init__.py`, et les modules de cartes
    # n'etaient JAMAIS lus. L'outil repondait « OK : tous les appels existent »
    # sans en avoir examine un seul. Mesure qui l'a etabli : reintroduire
    # `Faces.ShuffleAllToEncounterDeck` (methode inexistante, plantage reel en
    # partie sur bk013 Morph) laissait l'outil au vert.
    #
    # Les six packs plats historiques (`core`, `dt`...) etaient les seuls
    # reellement couverts — d'ou les deux prises citees plus haut.
    #
    # On parcourt donc recursivement, et on importe le namespace DU DOSSIER :
    # un module de carte fait `from . import *`, ce sont donc les noms de SON
    # set qu'il voit, pas ceux du pack parent.
    def dossiers_de_modules(pack: str):
        base = os.path.join(racine, "src", "cards", "pack", pack)
        for chemin, sous_dossiers, fichiers in os.walk(base):
            sous_dossiers[:] = [d for d in sous_dossiers if d != "__pycache__"]
            if not any(x.endswith(".py") and x != "__init__.py" for x in fichiers):
                continue
            relatif = os.path.relpath(chemin, os.path.join(racine, "src"))
            yield chemin, relatif.replace(os.sep, ".")

    lignes = []
    for pack in packs:
        for dossier, nom_module in dossiers_de_modules(pack):
            module_pack = __import__(nom_module, fromlist=["*"])
            for nom_fichier in sorted(os.listdir(dossier)):
                if not nom_fichier.endswith(".py"):
                    continue
                arbre = ast.parse(io.open(os.path.join(dossier, nom_fichier),
                                          encoding="utf-8").read())

                # Le type des variables, quand le module le declare par CastTo.
                #
                # ⚠ UNE VARIABLE EST LOCALE A SA FONCTION. Un fichier peut nommer
                # `this` dans dix fonctions, avec dix types differents — c'est le
                # cas de twc/__init__.py. Retenir le dernier vu faisait conclure sur
                # le mauvais type et signalait un appel parfaitement valide. On ne
                # garde donc un type QUE s'il est le seul declare pour ce nom dans
                # tout le fichier ; sinon on ne conclut pas.
                vus = {}
                for n in ast.walk(arbre):
                    if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) \
                            and isinstance(n.value.func, ast.Attribute) \
                            and n.value.func.attr == "CastTo" and n.value.args \
                            and isinstance(n.value.args[0], ast.Name) \
                            and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                        vus.setdefault(n.targets[0].id, set()).add(n.value.args[0].id)
                types_locaux = {nom: list(t)[0] for nom, t in vus.items() if len(t) == 1}

                for n in ast.walk(arbre):
                    if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)):
                        continue
                    base, methode = n.func.value, n.func.attr
                    if not isinstance(base, ast.Name):
                        continue
                    # ⚠ PIEGE : `from cards.pack import *` expose aussi des
                    # SOUS-MODULES du moteur, et leur nom ressemble a celui des
                    # variables des cartes — `player` est le module `game.player`,
                    # `message` le module `game.message`, `effect` le module
                    # `game.effect`. Les prendre pour la variable locale produisait
                    # 145 faux signalements. On ne garde donc que les CLASSES.
                    import types as _types
                    cible = getattr(module_pack, base.id, None)
                    if isinstance(cible, _types.ModuleType):
                        cible = None
                    if cible is None and base.id in types_locaux:
                        cible = getattr(module_pack, types_locaux[base.id], None)
                        if isinstance(cible, _types.ModuleType):
                            cible = None
                    if cible is None or not isinstance(cible, type):
                        continue  # variable dont on ignore le type : on ne conclut rien
                    if not hasattr(cible, methode):
                        lignes.append("%s/%s:%d  %s.%s n'existe pas"
                                      % (nom_module.replace("cards.pack.", ""),
                                         nom_fichier, n.lineno, base.id, methode))

    sys.stdout = vrai_stdout
    if lignes:
        print("\n".join(lignes))
        print("\n%d appel(s) inexistant(s)." % len(lignes))
    else:
        print("OK : tous les appels de %s existent." % ", ".join(packs))
    sys.stdout.flush()
    os._exit(1 if lignes else 0)


if __name__ == "__main__":
    sys.exit(main())
