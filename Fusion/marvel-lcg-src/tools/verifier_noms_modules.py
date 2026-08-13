"""Les noms qu'un module de carte utilise existent-ils vraiment ?

    python3.10 tools/verifier_noms_modules.py <game_dir> <pack> [pack ...]

Exemple :

    python3.10 tools/verifier_noms_modules.py ~/marvel-work/fusion/marvel-lcg-src/.game determination

POURQUOI CET OUTIL EXISTE
-------------------------
Entre `test_cards` et une partie reelle il reste un trou, et il est large.
`test_cards` appelle `GetAbilities()` : il attrape donc ce qui est evalue A LA
CONSTRUCTION de la liste de capacites. Mais le CORPS des fonctions internes
(l'operation d'une capacite, une condition, un lambda de choix) n'est execute
que lorsque la carte est REELLEMENT jouee. Un nom absent y dort tranquillement.

Trois pieges du projet passent exactement par ce trou :

  * ecrire `SetTarget(Character)` la ou le moteur attend la CHAINE "Character" —
    le nom n'existe pas, et rien ne le dit avant la partie ;
  * appeler une API « plausible » qui n'existe pas (`Faces.GetAll`,
    `player.DrawUpToHandSize`... voir les notes de methode) ;
  * oublier que `Filter`, `Worlds` ou `CanStatus` doivent venir du namespace du
    pack.

CE QU'IL FAIT
-------------
Il charge le moteur, lit le namespace REEL du pack (`dir(cards.pack.<pack>)`,
donc ce que `from . import *` donne aux modules), puis relit chaque module en
AST et signale tout nom charge qui n'est ni dans ce namespace, ni un builtin,
ni defini localement.

Il compte comme connus les imports LOCAUX (dans le corps d'une fonction) :
c'est un usage courant du jeu contre les imports circulaires.

CE QU'IL NE FAIT PAS
--------------------
Verifier qu'un ATTRIBUT existe (`Faces.GetAll` passe : `Faces` existe). Pour
cela, il n'y a que la lecture du moteur (`grep -rn "def <Nom>" src/game`) et la
partie reelle.
"""
import ast
import builtins
import io
import os
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    game_dir = os.path.expanduser(sys.argv[1])
    packs = sys.argv[2:]

    racine_src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "src", "cards", "pack")

    os.environ["RELEASE"] = "1"
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    # Le moteur parle beaucoup, et il redirige lui-meme la sortie : on garde le
    # vrai stdout de cote pour le resultat.
    vrai_stdout = sys.stdout
    journal = io.open("/tmp/verifier_noms_modules.log", "w")
    sys.stdout = sys.stderr = journal

    from engine import Engine
    Engine.Initialize()

    lignes = []
    for pack in packs:
        module_pack = __import__("cards.pack." + pack, fromlist=["*"])
        connus = set(dir(module_pack)) | set(dir(builtins))
        dossier = os.path.join(racine_src, pack)
        for nom_fichier in sorted(os.listdir(dossier)):
            if not nom_fichier.endswith(".py"):
                continue
            chemin = os.path.join(dossier, nom_fichier)
            arbre = ast.parse(io.open(chemin, encoding="utf-8").read())
            locaux = {n.id for n in ast.walk(arbre)
                      if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
            for n in ast.walk(arbre):
                if not isinstance(n, (ast.FunctionDef, ast.Lambda)):
                    continue
                arguments = list(n.args.args) + list(n.args.kwonlyargs) + list(n.args.posonlyargs)
                # `*args` et `**kwargs` comptent aussi : `def f(**criteres)`
                # rendait `criteres` inconnu (aoa/missions.py).
                arguments += [a for a in (n.args.vararg, n.args.kwarg) if a]
                locaux |= {a.arg for a in arguments}
            locaux |= {n.name for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef)}
            # Les imports LOCAUX comptent : la moitie du jeu ecrit
            # `from cards.database import CardsDB` dans le corps d'une fonction,
            # justement pour eviter un import circulaire au chargement.
            for n in ast.walk(arbre):
                if isinstance(n, (ast.Import, ast.ImportFrom)):
                    locaux |= {(a.asname or a.name).split(".")[0] for a in n.names}
            for n in ast.walk(arbre):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) \
                        and n.id not in connus and n.id not in locaux:
                    lignes.append("%s/%s:%d  nom inconnu : %s" % (pack, nom_fichier, n.lineno, n.id))

    sys.stdout = vrai_stdout
    if lignes:
        print("\n".join(lignes))
        print("\n%d nom(s) inconnu(s)." % len(lignes))
    else:
        print("OK : aucun nom inconnu dans %s." % ", ".join(packs))
    sys.stdout.flush()
    os._exit(1 if lignes else 0)


if __name__ == "__main__":
    sys.exit(main())
