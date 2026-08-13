"""Le module d'une carte est-il TROUVE, et sa capacite attachee ?

    python3.10 tools/sonde_capacites.py <game_dir> <port> <card_id> [card_id ...]

Exemple :

    python3.10 tools/sonde_capacites.py ~/marvel-work/fusion/marvel-lcg-src/.game 2397 \\
        01058 dt001 dt003

POURQUOI CETTE SONDE EXISTE
---------------------------
`test_generate_cards` prouve qu'une carte se CONSTRUIT, pas qu'elle a recupere
son module : une carte sans module se construit tres bien (sauf les Event, voir
factory.py). Un module mal place, mal nomme, ou dont le pack n'a pas de
`__init__.py` ne provoque AUCUNE erreur — la carte est simplement inerte.

CE QU'ELLE MESURE, ET COMMENT LA LIRE
-------------------------------------
Le nombre de capacites portees par les faces de la carte. Ce nombre n'a de sens
que COMPARE : une carte joueur en porte deja plusieurs qui viennent du moteur
(jouer, attaquer, dejouer...). Il faut donc toujours sonder ensemble :

  * un TEMOIN OFFICIEL qui a un module (ex. 01058, Daredevil) ;
  * une carte du meme type SANS module (ex. dt001 tant qu'il n'en a pas) ;
  * la carte que l'on vient d'ecrire.

Mesure du 13/08/2026 : allie sans module 7, allie avec module 8. Le module ajoute
exactement ses capacites, et l'ecart se lit d'un coup d'oeil.

CE QU'ELLE NE MESURE PAS
------------------------
Que la capacite FAIT la bonne chose. Les commandes lancees hors de la file du
moteur ne declenchent aucune reaction en chaine : seule une vraie partie le dit.
Cette sonde repond a « le module est-il branche ? », pas a « la carte
fonctionne-t-elle ? ».

PIEGES PAYES EN L'ECRIVANT
--------------------------
* les faces d'une carte sont dans `card.printed_faces` ; un `card.faces` qui
  n'existe pas renvoie 0 capacite pour TOUTES les cartes, temoin compris — d'ou
  la regle du temoin, qui a rendu l'erreur evidente ;
* il faut laisser tourner GameSetup/GameLoop dans un thread et ATTENDRE, sinon le
  monde n'est pas construit et `game.world` vaut None ;
* il faut sortir par `os._exit` comme le fait `test_cards.py`, sinon les threads
  non-daemon du moteur retiennent le processus indefiniment.
"""
import json
import os
import sys
import threading
import time


def Origine(ability) -> str:
    """Le module Python d'ou vient l'operation de la capacite.

    C'est ce qui repond quand le NOMBRE de capacites ne repond pas : une carte
    Resource ou Support voit son module REMPLACER la capacite que le moteur lui
    donnait, au lieu d'en ajouter une. Le compte ne bouge pas, l'origine si.
    """
    fn = getattr(ability, "operation", None)
    if fn is None:
        return "?"
    module = getattr(fn, "__module__", "?")
    # Le qualname porte la fabrique qui a ecrit l'operation
    # (`...DoubleResourcesThisGenerates.<locals>.the_power_of_leadership`) : c'est
    # LUI qui distingue deux capacites nees du meme fichier du moteur.
    noms = [Nom(fn)]
    # Une fabrique du moteur enveloppe souvent l'operation VOULUE dans une
    # operation generique : `CheckThisCanDropPay(the_power_of_leadership)` sort
    # un `add_to_pay_list` identique pour toutes les ressources, et la fonction
    # qui distingue dort dans sa fermeture. On descend donc d'un cran.
    for cellule in (fn.__closure__ or ()):
        try:
            valeur = cellule.cell_contents
        except ValueError:
            continue
        if callable(valeur) and getattr(valeur, "__qualname__", None):
            noms.append(Nom(valeur))
    return "%s : %s" % (module.split(".")[-1], " <- ".join(noms))


def Nom(fn) -> str:
    return getattr(fn, "__qualname__", getattr(fn, "__name__", "?")).replace(".<locals>.", " > ")


def main() -> int:
    if len([a for a in sys.argv[1:] if a != '--detail']) < 3:
        print(__doc__)
        return 2
    args = [a for a in sys.argv[1:] if a != "--detail"]
    detail = "--detail" in sys.argv[1:]
    game_dir = os.path.expanduser(args[0])
    port = int(args[1])
    cartes_voulues = args[2:]

    os.chdir(game_dir)
    sys.path.insert(0, game_dir)
    cfg_path = os.path.join(game_dir, "launch.json")
    cfg = json.load(open(cfg_path))
    cfg["server_addresses"] = ["127.0.0.1:%d" % port]
    json.dump(cfg, open(cfg_path, "w"), indent=2)

    # Le moteur parle beaucoup : on le range dans un journal pour ne garder que
    # le resultat sur la sortie standard.
    journal = open("/tmp/sonde_capacites.log", "w", buffering=1)
    vrai_stdout = sys.stdout
    sys.stdout = sys.stderr = journal

    lignes = []
    try:
        from engine import Engine
        Engine.Initialize()
        from game.scene.loader import SceneLoader
        scene = SceneLoader.NewScene("rhino", None, ["spider_man"], 42)
        game = Engine.game
        game.session.SetScene(scene, "Load")

        def tourner():
            try:
                if game.GameSetup():
                    game.GameLoop()
            except Exception:
                import traceback
                traceback.print_exc()

        threading.Thread(target=tourner, daemon=True).start()
        time.sleep(15)

        world = game.world
        from game.card.factory import CardFactory

        for card_id in cartes_voulues:
            try:
                carte = CardFactory.GenerateCard(card_id, world.area_removed, world)
                capacites = [a for f in carte.printed_faces for a in f.ability.abilities]
                ligne = "%-8s %d capacite(s)" % (card_id, len(capacites))
                if detail:
                    ligne += "\n" + "\n".join(
                        "             %-18s <- %s" % (a.type, Origine(a))
                        for a in capacites)
                lignes.append(ligne)
            except Exception as e:
                lignes.append("%-8s ECHEC %r" % (card_id, e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        lignes.append("ECHEC GENERAL %r (voir /tmp/sonde_capacites.log)" % (e,))

    sys.stdout = vrai_stdout
    print("\n".join(lignes))
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    sys.exit(main())
