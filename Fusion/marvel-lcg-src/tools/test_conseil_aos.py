"""Le Conseil executif d'Agents of S.H.I.E.L.D. entierement retourne.

Les trois cartes attachement (50181b, 50182b, 50183b) portent toutes le meme
texte : « If there are 3 [[Board Member]] attachments in play, the players lose
the game. » Le livret p.18 le redit pour Zemo : « If all of the board members
join Baron Zemo, the players lose the scenario. »

Le pack le cable en REPONSE A UN RETOURNEMENT, ce qui suffit tant que le
troisieme bascule en cours de partie. En campagne, non : les secrets se
reportent d'un scenario a l'autre, un membre a quatre secrets (trois en expert)
arrive DEJA retourne, et `Card.Flip` n'envoie `AfterCardFlip` que si
`world.is_game_started` — faux pendant la mise en place. Mesure avant
correction : les trois basculaient au setup, `game_over` restait faux, et comme
plus aucun retournement ne pouvait survenir la condition ne se declenchait
jamais. Les joueurs jouaient une partie deja perdue.

La condition est un ETAT, pas un evenement : on la relit une fois la mise en
place de campagne faite, a tous les scenarios.

Usage : python3.10 tools/test_conseil_aos.py [racine] [port]
"""
import json
import os
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.expanduser(
    "~/marvel-work/fusion/marvel-lcg-src")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 4900
SONDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonde_campagne.py")

TAUPE = "50185;50188;50191"
resultats = []
port = PORT


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def sonder(scenario, secrets):
    global port
    port += 1
    rapport = os.path.join(tempfile.gettempdir(), f"conseil_aos_{os.getpid()}_{port}.json")
    carnet = {"A.I.M. Envelope": TAUPE}
    for nom in ("Chief Medical Officer", "Chief Surveillance Officer", "Chief Tactical Officer"):
        carnet[f"Secret Counters: {nom}"] = str(secrets)
    env = dict(os.environ, RAPPORT=rapport, CAMPAIGN_LOG=json.dumps(carnet))
    for cle in ("FIN_DE_PARTIE", "PUZZLE", "CHOIX"):
        env.pop(cle, None)
    subprocess.run([sys.executable, SONDE, RACINE, scenario, "maria_hill", str(port)],
                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(rapport, encoding="utf-8") as f:
        sortie = json.load(f)
    os.remove(rapport)
    monde = sortie.get("monde") or {}
    attachements = sum(1 for z, v in monde.items() if isinstance(v, list)
                       for c in v if isinstance(c, dict)
                       and str(c.get("card_id", "")).endswith("b")
                       and str(c.get("card_id", ""))[:5] in ("50181", "50182", "50183"))
    return (sortie.get("erreurs") or [], bool(monde.get("game_over")),
            bool(monde.get("players_won")), attachements)


# 1. Expert, seuil a trois : les trois membres arrivent retournes.
erreurs, fini, gagne, att = sonder("baron_zemo_expert", 3)
verifier("expert : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("expert : les trois membres sont cote attachement", att == 3, att)
verifier("expert : la partie est perdue des la mise en place", fini and not gagne, (fini, gagne))

# 2. Expert sous le seuil. Un secret de depart seulement : le SOIN EXPERT en
#    pose un de plus (c'est son prix), donc deux secrets au maximum sur un
#    membre — sous les trois qui le feraient basculer. Mesure faite avec deux
#    secrets au depart : le soin en amenait un a trois et le retournait, ce qui
#    est le comportement juste et non un defaut.
erreurs, fini, gagne, att = sonder("baron_zemo_expert", 1)
verifier("expert, sous le seuil : aucun attachement", att == 0, att)
verifier("expert, sous le seuil : la partie continue", not fini, fini)

# 2 bis. Deux secrets reportes en expert : le soin en ajoute un et fait
#        basculer UN membre. Un seul ne perd pas la partie.
erreurs, fini, gagne, att = sonder("baron_zemo_expert", 2)
verifier("expert : le prix du soin peut faire basculer un membre", att == 1, att)
verifier("expert : un seul membre bascule ne perd pas la partie", not fini, fini)

# 3. Standard, seuil a quatre. Le scenario 3 prouve que la regle ne vaut pas
#    que pour Zemo : les trois cartes portent le texte.
erreurs, fini, gagne, att = sonder("modok", 4)
verifier("standard : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("standard, scenario 3 : la partie est perdue aussi",
         fini and not gagne and att == 3, (fini, gagne, att))

# 4. Standard a trois secrets : sous le seuil, rien ne bascule.
erreurs, fini, gagne, att = sonder("modok", 3)
verifier("standard, trois secrets : sous le seuil, rien ne bascule",
         att == 0 and not fini, (att, fini))

# 5. Le scenario 1 impose deux secrets a chacun et ignore le carnet : il ne
#    peut jamais commencer perdu.
erreurs, fini, gagne, att = sonder("black_widow", 4)
verifier("scenario 1 : le carnet est ignore, la partie commence normalement",
         not fini and att == 0, (fini, att))

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
