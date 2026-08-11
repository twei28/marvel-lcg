"""Le soin de campagne experte d'Agents of S.H.I.E.L.D.

Encarts SETUP des scenarios 2 a 5, sous « Expert Campaign Only » : « Each
player may place one secret counter on a Board Member environment to heal
damage from their identity equal to their REC. »

Les huit boites font toutes payer le retour a la sante, et jamais deux fois de
la meme facon. Ici le prix se paie sur le DECOR : un secret de plus sur le
Conseil, donc un pas de plus vers le basculement d'un membre du cote de Zemo.
Deux ecarts avec les sept autres, tous deux voulus par le livret — on soigne de
sa REC et non jusqu'aux PV imprimes, et le cout ne touche pas le deck du joueur.

Maria Hill sert de temoin : 9 PV imprimes, REC 3. Les comptes sont donc lisibles
a la main, et un soin qui se tromperait de valeur (PV pleins au lieu de REC) se
verrait tout de suite.

Le pilote de la sonde accepte toujours la premiere option legale, donc le soin
est PRIS quand il est propose. Ce qui se mesure ici, c'est donc : est-il propose
au bon moment, dans le bon ordre, et au bon prix.

Usage : python3.10 tools/test_soin_expert_aos.py [racine] [port]
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
PV_IMPRIMES = 9
REC = 3

resultats = []
port = PORT


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def sonder(scenario, carnet):
    global port
    port += 1
    rapport = os.path.join(tempfile.gettempdir(), f"soin_aos_{os.getpid()}_{port}.json")
    env = dict(os.environ, RAPPORT=rapport, CAMPAIGN_LOG=json.dumps(carnet))
    env.pop("FIN_DE_PARTIE", None)
    env.pop("PUZZLE", None)
    subprocess.run([sys.executable, SONDE, RACINE, scenario, "maria_hill", str(port)],
                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(rapport, encoding="utf-8") as f:
        sortie = json.load(f)
    os.remove(rapport)
    monde = sortie.get("monde") or {}
    joueur = (monde.get("players") or [{}])[0]
    pv = [(c.get("info") or {}).get("health") for c in (joueur.get("area_hero") or [])]
    conseil = {c["card_id"]: c["info"].get("c_secret", 0)
               for c in (monde.get("area_environment") or [])
               if c["card_id"].startswith(("50181", "50182", "50183"))}
    return (sortie.get("erreurs") or [], (pv[0] if pv else None), conseil,
            bool(monde.get("game_over")))


# 1. Le cas nominal : PV reportes bas, soin pris, prix paye.
erreurs, pv, conseil, fini = sonder("batroc_expert", {"A.I.M. Envelope": TAUPE,
                                                "Player 1 Remaining hit points": "3"})
verifier("expert : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("l'identite est soignee de sa REC, pas remise a neuf",
         pv == 3 + REC, (pv, 3 + REC))
verifier("le soin coute UN secret, pose sur un seul membre",
         sum(conseil.values()) == 1, conseil)

# 2. Le plafond : on ne depasse jamais les PV imprimes.
erreurs, pv, conseil, fini = sonder("batroc_expert", {"A.I.M. Envelope": TAUPE,
                                                "Player 1 Remaining hit points": "8"})
verifier("le soin ne depasse pas les PV imprimes", pv == PV_IMPRIMES, pv)

# 3. Temoin : en standard, ni report ni soin.
erreurs, pv, conseil, fini = sonder("batroc", {"A.I.M. Envelope": TAUPE,
                                         "Player 1 Remaining hit points": "3"})
verifier("standard : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("standard : aucun report de PV, donc aucun soin", pv == PV_IMPRIMES, pv)
verifier("standard : aucun secret pose en paiement",
         sum(conseil.values()) == 0, conseil)

# 4. Temoin : le scenario 1 n'a pas cette instruction (rien a reporter encore).
erreurs, pv, conseil, fini = sonder("black_widow_expert", {"A.I.M. Envelope": TAUPE})
verifier("scenario 1 expert : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("scenario 1 expert : pas de soin, l'identite part entiere",
         pv == PV_IMPRIMES, pv)
verifier("scenario 1 expert : le Conseil garde ses deux secrets de depart",
         sorted(conseil.values()) == [2, 2, 2], conseil)

# 5. Le Conseil entierement bascule. La question du soin ne se pose meme plus :
#    trois attachements [[Board Member]] en jeu perdent la partie des la mise en
#    place (voir tools/test_conseil_aos.py), qui s'arrete donc avant de reporter
#    les PV et avant d'offrir le soin. Ce cas disait le contraire jusqu'au
#    11/8/2026, parce que la regle des trois attachements ne s'appliquait pas
#    encore a la mise en place.
erreurs, pv, conseil, fini = sonder("baron_zemo_expert", {
    "A.I.M. Envelope": TAUPE,
    "Player 1 Remaining hit points": "2",
    "Secret Counters: Chief Medical Officer": "3",
    "Secret Counters: Chief Surveillance Officer": "3",
    "Secret Counters: Chief Tactical Officer": "3"})
verifier("Conseil bascule : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("Conseil bascule : plus aucun environnement [[Board Member]]",
         conseil == {}, conseil)
verifier("Conseil bascule : la partie est perdue des la mise en place", fini, fini)
verifier("Conseil bascule : ni report de PV ni soin, la mise en place s'arrete",
         pv == PV_IMPRIMES, pv)

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
