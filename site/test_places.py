"""Le nombre de places est écrit à TROIS endroits : ils doivent s'accorder.

⚠ POURQUOI CE FICHIER EXISTE (18/09/2026). Passer de 20 à 30 places demande
trois changements, dans trois fichiers qui ne se connaissent pas :

  1. `NB_EMPLACEMENTS` (site/orchestrateur.py) : combien de places le site
     attribue ;
  2. `PLACES_MAX` (Fusion/.../tools/config_serveur.py) : au-delà, le moteur
     REFUSE de fabriquer la configuration d'une table ;
  3. les routes `p1..pN` du Caddyfile : sans route, une table tourne sur son
     port et personne ne peut la joindre.

Chacun tout seul donne une panne différente, et aucune ne se voit avant qu'un
joueur tombe dessus : une place sans route Caddy ouvre une table injoignable,
une place au-delà de `PLACES_MAX` lève une erreur à l'ouverture.

Usage : python3 site/test_places.py
"""
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
CADDYFILE = os.path.join(RACINE, "deploiement", "Caddyfile")
CONFIG_SERVEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "tools", "config_serveur.py")
ORCHESTRATEUR = os.path.join(ICI, "orchestrateur.py")

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom
          + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


def nombre(chemin, motif) -> int:
    texte = open(chemin, encoding="utf-8").read()
    trouve = re.search(motif, texte, re.M)
    return int(trouve.group(1)) if trouve else -1


places_site = nombre(ORCHESTRATEUR, r'NB_EMPLACEMENTS = int\(os\.environ\.get\("NB_EMPLACEMENTS", "(\d+)"\)\)')
places_moteur = nombre(CONFIG_SERVEUR, r"^PLACES_MAX = (\d+)")

caddy = open(CADDYFILE, encoding="utf-8").read()
routes = sorted(int(n) for n in re.findall(r"@p(\d+) host", caddy))
ports = sorted(int(n) for n in re.findall(r"reverse_proxy 127\.0\.0\.1:(23\d\d)", caddy))

print("Les trois plafonds de places s'accordent")
verifier("le site et le moteur annoncent le meme nombre",
         places_site == places_moteur,
         "site=%s moteur=%s" % (places_site, places_moteur))
verifier("le Caddyfile porte autant de routes que de places",
         len(routes) == places_site,
         "routes=%d places=%s" % (len(routes), places_site))
verifier("les routes vont de 1 a N, sans trou",
         routes == list(range(1, places_site + 1)),
         "manquantes : %s" % sorted(set(range(1, places_site + 1)) - set(routes)))

# ⚠ LE PORT EST DEDUIT DE LA PLACE (PORT_BASE + N, orchestrateur.py). Une route
# `p7` qui pointerait vers le port de `p8` enverrait un joueur sur la table
# d'un autre : c'est la seule erreur de ce fichier qui ne se verrait pas tout
# de suite, et la plus grave.
attendus = [2350 + n for n in routes]
verifier("chaque route vise le port de SA place", ports == attendus,
         "attendus %s... obtenus %s..." % (attendus[:3], ports[:3]))

print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
