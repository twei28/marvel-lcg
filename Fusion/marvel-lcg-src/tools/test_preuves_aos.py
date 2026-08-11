"""Les preuves d'Agents of S.H.I.E.L.D., mesurees sur de vraies parties.

Deux regles a tenir, et elles se contredisent presque :

* le moteur DOIT lire la combinaison de la taupe (`A.I.M. Envelope`), sans
  quoi il ne sait pas quelles preuves sont dans l'enveloppe S.H.I.E.L.D. ;
* le JOUEUR ne doit JAMAIS la lire, alors que le carnet sortant lui est
  presente tel quel a la fin de chaque partie.

Deux volets. Le premier GAGNE les preuves : il monte une partie du scenario 1,
vide (ou non) le Medecin en chef de ses secrets par une commande Puzzle,
declenche la fin de partie, et relit le carnet SORTANT. Le second les POSE :
il monte les scenarios 2 et 5 avec des preuves deja gagnees au carnet entrant,
et regarde l'aire des preuves et la main du joueur apres la mise en place.

Cas et temoins vont par paires : la table est identique, seul le carnet
ENTRANT change, donc l'ecart mesure ne peut venir que de lui.

Le cas « fuite » merite un mot : il injecte une cle bidon par la meme voie que
le secret. Elle ressort, le secret non — c'est ce qui prouve que le filtre de
`CLES_SECRETES` fait le travail, et pas que le secret n'ait simplement jamais
atteint le store.

Usage: python3.10 tools/test_preuves_aos.py [racine] [port]
  racine : dossier qui contient .game (defaut : ~/marvel-work/fusion/marvel-lcg-src)
"""
import json
import os
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.expanduser(
    "~/marvel-work/fusion/marvel-lcg-src")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 4600
SONDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonde_campagne.py")
VIDER = "Puzzle.Counter('Chief Medical Officer', 'secret', -2)"

TAUPE = "50185;50188;50191"          # une preuve par serie : moyen, mobile, occasion
ENVELOPPE = ('50186', '50187', '50189', '50190', '50192', '50193')  # les six autres

resultats = []
port = PORT


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def sonder(carnet, puzzle):
    """Une partie complete, et le carnet sortant qu'elle a produit."""
    global port
    port += 1
    rapport = os.path.join(tempfile.gettempdir(), f"preuves_aos_{os.getpid()}_{port}.json")
    env = dict(os.environ,
               RAPPORT=rapport,
               FIN_DE_PARTIE="1",
               CAMPAIGN_LOG=json.dumps(carnet),
               PUZZLE=json.dumps(puzzle))
    subprocess.run([sys.executable, SONDE, RACINE, "black_widow", "maria_hill", str(port)],
                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(rapport, encoding="utf-8") as f:
        sortie = json.load(f)
    os.remove(rapport)
    carnet_sortant = sortie.get("carnet_sortant") or {}
    return sortie.get("erreurs") or [], carnet_sortant.get("suggestions") or {}


def sonder_monde(scenario, carnet):
    """Une mise en place, et le monde qu'elle produit. Pas de fin de partie."""
    global port
    port += 1
    rapport = os.path.join(tempfile.gettempdir(), f"preuves_aos_{os.getpid()}_{port}.json")
    env = dict(os.environ, RAPPORT=rapport, CAMPAIGN_LOG=json.dumps(carnet))
    env.pop("FIN_DE_PARTIE", None)
    env.pop("PUZZLE", None)
    subprocess.run([sys.executable, SONDE, RACINE, scenario, "maria_hill", str(port)],
                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(rapport, encoding="utf-8") as f:
        sortie = json.load(f)
    os.remove(rapport)
    return sortie.get("erreurs") or [], sortie.get("monde") or {}


def en_jeu(monde):
    return sorted(c["card_id"] for c in monde.get("area_evidence", []))


def taille_main(monde):
    return len(monde["players"][0].get("hand_cards", []))


def preuves(carnet):
    valeur = carnet.get("Evidence Gained")
    return [x for x in (valeur or "").split(";") if x]


# 1. Un membre vide, le secret en place : une preuve, et jamais celle de la taupe.
erreurs, carnet = sonder({"A.I.M. Envelope": TAUPE}, [VIDER])
verifier("cas nominal : la partie tourne sans erreur", not erreurs, erreurs)
gagnees = preuves(carnet)
verifier("un membre vide rapporte une preuve", len(gagnees) == 1, gagnees)
verifier("la preuve sort de l'enveloppe S.H.I.E.L.D.",
         all(p in ENVELOPPE for p in gagnees), gagnees)
verifier("le membre vide est bien note a zero",
         carnet.get("Secret Counters: Chief Medical Officer") == "0",
         carnet.get("Secret Counters: Chief Medical Officer"))

# 2. Temoin : meme table, mais aucun membre vide.
_, carnet = sonder({"A.I.M. Envelope": TAUPE}, [])
verifier("aucun membre vide : aucune preuve", not preuves(carnet), preuves(carnet))

# 3. Temoin : meme table, mais pas de secret injecte. Sans lui on ne sait pas
#    quelles preuves sont dans l'enveloppe S.H.I.E.L.D., donc on n'en donne
#    aucune. C'est ce cas qui PROUVE que l'injection est lue.
_, carnet = sonder({}, [VIDER])
verifier("sans l'enveloppe A.I.M., aucune preuve n'est donnee",
         not preuves(carnet), preuves(carnet))

# 4. Cumul : la liste grossit d'une preuve, elle ne se remplace pas.
deja = ";".join(ENVELOPPE[:4])
_, carnet = sonder({"A.I.M. Envelope": TAUPE, "Evidence Gained": deja}, [VIDER])
gagnees = preuves(carnet)
verifier("les preuves deja gagnees sont conservees",
         gagnees[:4] == list(ENVELOPPE[:4]), gagnees)
verifier("une seule preuve s'ajoute", len(gagnees) == 5, gagnees)
verifier("jamais deux fois la meme", len(set(gagnees)) == len(gagnees), gagnees)

# 5. Enveloppe epuisee : les six sont la, rien ne s'ajoute et rien ne casse.
toutes = ";".join(ENVELOPPE)
erreurs, carnet = sonder({"A.I.M. Envelope": TAUPE, "Evidence Gained": toutes}, [VIDER])
verifier("enveloppe epuisee : la partie tourne sans erreur", not erreurs, erreurs)
verifier("enveloppe epuisee : la liste ne bouge plus",
         preuves(carnet) == list(ENVELOPPE), preuves(carnet))

# 6. Le secret ne ressort pas — et le temoin injecte, lui, ressort.
_, carnet = sonder({"A.I.M. Envelope": TAUPE, "Temoin Injecte": "visible"}, [VIDER])
verifier("une cle injectee ressort bien au carnet",
         carnet.get("Temoin Injecte") == "visible", carnet.get("Temoin Injecte"))
verifier("la combinaison de la taupe, elle, est filtree",
         "A.I.M. Envelope" not in carnet, carnet.get("A.I.M. Envelope"))

# ---------------------------------------------------------------------------
# Second volet : les preuves gagnees se posent au scenario suivant.
# Livret, encarts SETUP des scenarios 2 a 5 : « After resolving mulligans,
# resolve the "Setup" ability of each evidence card the players have earned. »
# On prend Wiretap (50186, allie Justice) et Travel (50192, soutien Justice) :
# deux capacites que le deck de depart de Maria Hill peut vraiment satisfaire.
DEUX = "50186;50192"

# 7. Scenario 2 sans aucune preuve : la reference.
erreurs, monde = sonder_monde("batroc", {"A.I.M. Envelope": TAUPE})
verifier("scenario 2 nu : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("scenario 2 nu : aucune preuve en jeu", not en_jeu(monde), en_jeu(monde))
main_nue = taille_main(monde)
secrets_nus = sum(c["info"].get("c_secret", 0) for c in monde.get("area_environment", [])
                  if c["card_id"].startswith(("50181", "50182", "50183")))
verifier("scenario 2 nu : aucun secret sur le Conseil", secrets_nus == 0, secrets_nus)

# 8. Meme scenario, deux preuves gagnees.
erreurs, monde = sonder_monde("batroc", {"A.I.M. Envelope": TAUPE, "Evidence Gained": DEUX})
verifier("scenario 2 : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("les deux preuves gagnees sont en jeu, et elles seules",
         en_jeu(monde) == ["50186", "50192"], en_jeu(monde))
# Chaque preuve propose deux choses : poser un secret sur un membre du Conseil,
# et ajouter une carte cherchee A LA MAIN. Le pilote de la sonde accepte tout ce
# qui est legal, donc les deux partent. La main doit grossir d'autant, ce qui ne
# peut arriver QU'APRES la pioche et le mulligan : c'est la preuve que l'etape
# 15 bis est au bon endroit.
verifier("la main grossit d'une carte par preuve, apres le mulligan",
         taille_main(monde) == main_nue + 2, (main_nue, taille_main(monde)))
secrets = sum(c["info"].get("c_secret", 0) for c in monde.get("area_environment", [])
              if c["card_id"].startswith(("50181", "50182", "50183")))
verifier("chaque preuve pose un secret sur un membre du Conseil", secrets == 2, secrets)

# 9. Scenario 5 : son set apporte les NEUF preuves. Seules les gagnees doivent
#    rester, sinon les trois de l'enveloppe A.I.M. donnaient la taupe au joueur.
erreurs, monde = sonder_monde("baron_zemo", {"A.I.M. Envelope": TAUPE, "Evidence Gained": DEUX})
verifier("scenario 5 : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("scenario 5 : les neuf preuves du set ne debarquent plus",
         en_jeu(monde) == ["50186", "50192"], en_jeu(monde))
verifier("scenario 5 : aucune preuve de l'enveloppe A.I.M. en jeu",
         not [p for p in en_jeu(monde) if p in TAUPE.split(";")], en_jeu(monde))

# 10. Une valeur inconnue au carnet ne fait rien entrer en jeu.
erreurs, monde = sonder_monde("batroc", {"A.I.M. Envelope": TAUPE,
                                         "Evidence Gained": "50186;99999"})
verifier("une preuve inconnue est ignoree sans casser la mise en place",
         not erreurs and en_jeu(monde) == ["50186"], (erreurs, en_jeu(monde)))

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
