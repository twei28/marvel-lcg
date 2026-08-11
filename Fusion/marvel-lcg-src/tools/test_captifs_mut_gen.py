"""Les allies CAPTIVE de Mutant Genesis : « may be shuffled into any deck ».

Livret mc32, encarts des scenarios 3, 4 et 5 (p.12, 16, 19) : « Each CAPTIVE
ally recorded in the campaign log MAY be shuffled into ANY player's deck. »

Deux libertes, et le code n'en offrait aucune : tout partait d'office chez le
premier joueur. C'etait le dernier ecart de regle ouvert sur les huit boites.

Ce qui se mesure ici, et pourquoi la taille des decks ne suffit pas
---------------------------------------------------------------------
Le pilote de la sonde repond la premiere option legale a CHAQUE question, ce
qui rend une seule branche observable : avec ce seul reglage, un menu a une
branche et un menu a quatre se mesurent pareil. D'ou `CHOIX`, qui deplace le
curseur dans la liste des options. Mais `CHOIX` change AUSSI les mulligans,
donc la taille d'un deck ne veut plus rien dire d'une mesure a l'autre. On
compte donc les CARTES elles-memes, ou qu'elles soient.

Trois branches, trois resultats attendus :
  CHOIX=0   les captifs vont dans le deck du premier joueur
  CHOIX=1   ils vont dans le deck du SECOND — « any player's deck »
  CHOIX=-1  la derniere option est « Cancel » : aucun captif nulle part — « may »

Et un defaut PREEXISTANT, corrige au passage : `Faces.ShuffleAllTo` ne melange
que s'il a deplace quelque chose. Les cartes etant generees directement DANS le
deck, rien ne bougeait, le melange ne partait jamais et les quatre captifs se
retrouvaient dans la MAIN DE DEPART. C'est le dernier cas ci-dessous.

Usage : python3.10 tools/test_captifs_mut_gen.py [racine] [port]
"""
import json
import os
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.expanduser(
    "~/marvel-work/fusion/marvel-lcg-src")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 4800
SONDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonde_campagne.py")

# Rictor, Boom Boom, Cannonball et Wolfsbane, les quatre CAPTIVE du set
# Project Wideawake. Le scenario 3 est le premier a les rendre.
CAPTIFS = ("32089", "32090", "32091", "32092")
SCENARIO = "master_mold"
EQUIPE = "colossus,cyclops"

resultats = []
port = PORT


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def sonder(carnet, choix=0, equipe=EQUIPE):
    global port
    port += 1
    rapport = os.path.join(tempfile.gettempdir(), f"captifs_mg_{os.getpid()}_{port}.json")
    env = dict(os.environ, RAPPORT=rapport, CAMPAIGN_LOG=json.dumps(carnet), CHOIX=str(choix))
    env.pop("FIN_DE_PARTIE", None)
    env.pop("PUZZLE", None)
    subprocess.run([sys.executable, SONDE, RACINE, SCENARIO, equipe, str(port)],
                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(rapport, encoding="utf-8") as f:
        sortie = json.load(f)
    os.remove(rapport)
    return sortie.get("erreurs") or [], (sortie.get("monde") or {})


def ou_sont(monde):
    """Les captifs, par emplacement : {(joueur, zone): [ids]}."""
    trouves = {}
    for i, joueur in enumerate(monde.get("players") or []):
        for zone, contenu in joueur.items():
            if isinstance(contenu, list):
                ids = sorted(c.get("card_id") for c in contenu
                             if isinstance(c, dict) and str(c.get("card_id", "")) in CAPTIFS)
                if ids:
                    trouves[(i, zone)] = ids
    for zone, contenu in monde.items():
        if isinstance(contenu, list):
            plat = [c for y in contenu for c in (y if isinstance(y, list) else [y])
                    if isinstance(c, dict)]
            ids = sorted(c.get("card_id") for c in plat if str(c.get("card_id", "")) in CAPTIFS)
            if ids:
                trouves[("monde", zone)] = ids
    return trouves


CARNET = {"Captive Allies": ";".join(CAPTIFS)}

# 1. Premiere option : le deck du premier joueur. C'est l'ancien comportement,
#    qui reste une reponse possible parmi d'autres.
erreurs, monde = sonder(CARNET, choix=0)
place = ou_sont(monde)
verifier("premier joueur : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("premier joueur : les quatre captifs dans SON deck",
         place.get((0, "player_deck")) == list(CAPTIFS), place)
verifier("premier joueur : aucun captif ailleurs", len(place) == 1, place)

# 2. Deuxieme option : le deck du SECOND joueur. C'est « any player's deck »,
#    et c'est ce que le code ne savait pas faire.
erreurs, monde = sonder(CARNET, choix=1)
place = ou_sont(monde)
verifier("second joueur : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("second joueur : les quatre captifs dans SON deck",
         place.get((1, "player_deck")) == list(CAPTIFS), place)
verifier("second joueur : rien chez le premier",
         not [k for k in place if k[0] == 0], place)

# 3. Derniere option : « Cancel ». C'est le « may » du livret.
erreurs, monde = sonder(CARNET, choix=-1)
place = ou_sont(monde)
verifier("refus : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("refus : aucun captif nulle part", place == {}, place)

# 4. Temoin : sans carnet, aucune question et aucun captif.
erreurs, monde = sonder({}, choix=0)
verifier("carnet vide : aucun captif", ou_sont(monde) == {}, ou_sont(monde))

# 5. Le melange part vraiment. Les captifs generes DANS le deck ne
#    declenchaient pas `deck.Shuffle` : ils restaient sur le dessus et
#    partaient droit dans la main de depart, les quatre a la fois.
erreurs, monde = sonder(CARNET, choix=0)
place = ou_sont(monde)
verifier("aucun captif dans la main de depart",
         not [k for k in place if k[1] == "hand_cards"], place)

# 6. Un identifiant inconnu au carnet ne doit pas casser la mise en place.
erreurs, monde = sonder({"Captive Allies": "32089;99999"}, choix=0)
place = ou_sont(monde)
verifier("un identifiant inconnu est ignore sans casser la mise en place",
         not erreurs and place.get((0, "player_deck")) == ["32089"], (erreurs, place))

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
