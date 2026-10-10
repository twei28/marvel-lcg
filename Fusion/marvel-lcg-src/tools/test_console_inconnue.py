"""Une commande de console inconnue ne doit pas faire tomber le moteur.

Usage:
    ~/marvel-work/python/bin/python3.10 tools/test_console_inconnue.py \
        .game-src-par8 45300 [nom_du_cas]

La console du plateau passe par `/debug?<texte>` (server_sync.py) :
`Console.SetCommand` puis `Console.Execute`, qui `exec` le texte tel quel.
Un nom inconnu levait une NameError jusqu'a la boucle du jeu. Meme harnais
que tools/test_mode_manuel.py, un processus par cas.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_mode_manuel import id_du_vilain, monter_le_moteur  # noqa: E402


def executer_console(jeu, monde, texte):
    """Ce que fait la route /debug? puis la boucle du controleur."""
    console = jeu.controller_manager.console
    console.SetCommand(texte, monde)
    return console.Execute("", monde, [])


def cas_commande_inconnue(game_dir, port):
    """Le REFUS : un nom inconnu ne leve plus, et l'erreur est signalee."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    signalees = []
    origine = monde.render.ErrorOccurred
    monde.render.ErrorOccurred = lambda info: (signalees.append(info), origine(info))
    executer_console(jeu, monde, "commande_qui_n_existe_pas")
    assert signalees, "l'erreur de la commande n'a pas ete signalee au plateau"
    assert jeu.controller_manager.console.debug_cmds == "", \
        "la commande ratee est restee en attente"
    return "une commande inconnue est signalee sans faire tomber le moteur"


def cas_commande_valide(game_dir, port):
    """Le temoin : une commande valide s'execute toujours."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    # Deux executeurs selon la scene (Console.Execute) : `Puzzle` pour
    # PuzzleHelper.Exec, `puzzle` pour RunCheat.
    nom = "Puzzle" if monde.scene.is_puzzle else "puzzle"
    executer_console(jeu, monde, f"{nom}.Damage({vilain}, 2)")
    perdus = monde.object_manager.card_dict[vilain].face.GetLostHealth()
    assert perdus == 2, f"la commande valide n'a pas ete executee : {perdus}"
    return "une commande valide s'execute toujours"


CAS = {
    "commande_inconnue": cas_commande_inconnue,
    "commande_valide": cas_commande_valide,
}


def main():
    game_dir, port = sys.argv[1], int(sys.argv[2])
    voulu = sys.argv[3] if len(sys.argv) > 3 else None
    noms = [voulu] if voulu else list(CAS)
    for rang, nom in enumerate(noms):
        fils = subprocess.run(
            [sys.executable, os.path.abspath(__file__), game_dir,
             str(port + rang), nom, "--fils"],
            capture_output=True, text=True, timeout=300)
        verdict = "VERT" if fils.returncode == 0 else "ROUGE"
        print(f"{verdict} : {nom}")
        if fils.returncode != 0:
            print(fils.stdout[-3000:])
            print(fils.stderr[-3000:])
            sys.exit(1)


if __name__ == "__main__":
    if "--fils" in sys.argv:
        try:
            resultat = CAS[sys.argv[3]](sys.argv[1], int(sys.argv[2]))
        except BaseException:
            import traceback
            traceback.print_exc()
            os._exit(1)
        print(resultat)
        os._exit(0)
    main()
