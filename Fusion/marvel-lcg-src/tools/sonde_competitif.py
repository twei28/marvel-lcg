"""Sonde du mode competitif : monte une partie a deux camps et decrit ce qui existe.

Ce que la sonde MESURE, table par table : le complot principal en jeu, le
leader, la taille du deck rencontre, et les joueurs assis. C'est la seule
maniere de savoir si les deux tables sont vraiment distinctes, parce que le
moteur ne se plaint pas quand tout atterrit dans la meme zone : il joue.

Ce qu'elle NE DIT PAS : qu'une partie competitive se joue correctement. Les
phases ne sont pas encore enfilees par camp, les conditions de victoire pas
encore separees.

Usage :
    python3.10 tools/sonde_competitif.py <game_dir absolu> \
        [--camp1 iron_man] [--camp2 captain_america] \
        [--deck1 tigra] [--deck2 hulkling] [--rounds 0]

Python 3.10 : ~/marvel-work/python/bin/python3.10
"""
import argparse, json, os, sys

os.environ.setdefault("RELEASE", "1")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("game_dir")
    ap.add_argument("--camp1", default="iron_man")
    ap.add_argument("--camp2", default="captain_america")
    ap.add_argument("--deck1", default="tigra")
    ap.add_argument("--deck2", default="hulkling")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--rounds", type=int, default=0)
    args = ap.parse_args()

    game_dir = os.path.abspath(os.path.expanduser(args.game_dir))
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)
    sys.argv = [sys.argv[0], "-config_files", "launch.json", "-device", "key"]

    from engine.device.manager.base import DeviceManager

    # Le moteur pose des questions des la mise en place. Repondre « 0 » a tout
    # ne marche PAS : une question forcee (le Setup d'un leader, qui cherche
    # une carte dans le deck) n'accepte pas le vide, et le moteur la repose
    # sans fin. Le pilote de la sonde prend donc la premiere option legale et
    # lui donne le nombre de cibles exige.
    passer = json.dumps({"id": "0", "targets": [], "resources": []})

    compteur = {"questions": 0}

    def pilote(self, data, player_id, check):
        compteur["questions"] += 1
        if compteur["questions"] > 20000:
            raise SystemExit("sonde : plafond de questions atteint")
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            return passer
        libres = [o for o in options
                  if isinstance(o, dict) and not o.get("failure_reason")]
        if not libres:
            return passer
        choix = libres[0]
        legales = [str(x) for x in (choix.get("all_legal_targets") or [])]
        plage = choix.get("target_num_range") or [0, 0]
        mini = plage[0] if isinstance(plage[0], int) else 0
        return json.dumps({
            "id": str(choix.get("id", 0)),
            "targets": legales[:mini],
            "resources": [],
        })

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, player_id, check: None
    DeviceManager.DoWaitSync = lambda self, player_id, check: None

    from engine import Engine
    Engine.Initialize()
    from engine.file.manager import FileManager
    from engine.lib import Json
    from game.scene.replay import CampaignDescriptor
    from game.game_run.game_new import NewGameDescriptor

    def lire_json(genre: str, nom: str) -> str:
        chemin = FileManager.FindJsonPath(genre, nom)
        assert chemin, f"{genre} introuvable : {nom}"
        with FileManager.OpenFile(chemin, read=True) as fichier:
            return fichier.Read()

    def sets_de_rencontre(texte: str) -> 'List[str]':
        """Ce que l'ecran de preparation envoie : les sets du scenario plus ses
        modulaires recommandes, dedupliques."""
        campagne = Json.LoadsAs(texte, CampaignDescriptor)
        campagne.UpdateVersion()
        vus, sortie = set(), []
        for nom in list(campagne.encounter_sets) + list(campagne.modular_sets):
            if nom not in vus:
                vus.add(nom)
                sortie.append(nom)
        return sortie

    camp1 = lire_json("Campaign", args.camp1)
    camp2 = lire_json("Campaign", args.camp2)

    # La sonde passe par le VRAI contrat de lancement, celui que remplit
    # l'ecran de preparation : sans cela elle prouverait que le moteur sait
    # monter deux tables, pas qu'on sait les lui demander.
    descripteur = NewGameDescriptor(
        campaign_json=camp1,
        encounter_set_names=sets_de_rencontre(camp1),
        hero_json=[lire_json("Hero", args.deck1), lire_json("Hero", args.deck2)],
        seed=args.graine,
        timeout=0,
        challenges=[],
        rules=["mode_competitive"],
        campaign_log={},
        campaign_json_2=camp2,
        encounter_set_names_2=sets_de_rencontre(camp2),
        teams=[0, 1],
    )

    jeu = Engine.game
    jeu.session.NewGame(descripteur)
    if not jeu.GameSetup():
        print("ECHEC : GameSetup a rendu faux")
        return 1

    monde = jeu.world
    from game.operate.worlds import Worlds

    print(f"zones de jeu : {len(monde.game_areas)}")
    rapport = []
    for i, zone in enumerate(monde.game_areas):
        joueurs = [j.GetIdentity().name for j in monde.GetTeamPlayers(i)]
        complots = [s.name for s in Worlds.GetMainSchemes(zone)]
        leader = monde.GetScenario().GetVillain(zone)
        deck = getattr(leader, "encounter_deck", None) if leader else None
        rapport.append({
            "camp": i,
            "joueurs": joueurs,
            "complots": complots,
            "leader": leader.name if leader else None,
            "pv_leader": getattr(leader, "health", None) if leader else None,
            "deck_rencontre": deck.GetSize() if deck else None,
            "id_deck_rencontre": id(deck) if deck else None,
        })
        print(f"  camp {i} : joueurs={joueurs} complots={complots} "
              f"leader={rapport[-1]['leader']} pv={rapport[-1]['pv_leader']} "
              f"deck_rencontre={rapport[-1]['deck_rencontre']}")

    verdicts = []
    if len(monde.game_areas) != 2:
        verdicts.append("les deux camps ne sont pas dans deux zones")
    if len({r["leader"] for r in rapport}) != 2:
        verdicts.append("les deux camps n'ont pas deux leaders differents")
    if len({r["id_deck_rencontre"] for r in rapport}) != 2:
        verdicts.append("les deux camps partagent le meme deck rencontre")
    if any(not r["joueurs"] for r in rapport):
        verdicts.append("un camp n'a aucun joueur")
    if any(len(r["complots"]) != 1 for r in rapport):
        verdicts.append("un camp n'a pas exactement un complot principal")

    if args.rounds:
        # `GameLoop` mene la partie jusqu'a sa fin : la sonde ne sait pas
        # jouer, elle passe a chaque question. C'est un test de survie du
        # moteur, pas une mesure de jeu.
        jeu.GameLoop()
        print(f"partie menee : round {monde.round_id}, "
              f"fin = {getattr(monde.game_over, 'reason', None)}")

    print("VERDICT :", "la preparation a deux camps tient" if not verdicts
          else " / ".join(verdicts))
    return 0 if not verdicts else 2


if __name__ == "__main__":
    sys.exit(main())
