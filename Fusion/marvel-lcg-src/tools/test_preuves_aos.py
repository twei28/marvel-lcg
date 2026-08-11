"""Les preuves d'Agents of S.H.I.E.L.D., mesurees sur de vraies parties.

Deux regles a tenir, et elles se contredisent presque :

* le moteur DOIT lire la combinaison de la taupe (`A.I.M. Envelope`), sans
  quoi il ne sait pas quelles preuves sont dans l'enveloppe S.H.I.E.L.D. ;
* le JOUEUR ne doit JAMAIS la lire, alors que le carnet sortant lui est
  presente tel quel a la fin de chaque partie.

Chaque cas monte une partie du scenario 1, vide (ou non) le Medecin en chef de
ses secrets par une commande Puzzle, declenche la fin de partie, et relit le
carnet SORTANT. Cas et temoins vont par paires : la table est identique, seul
le carnet ENTRANT change, donc l'ecart mesure ne peut venir que de lui.

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

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
