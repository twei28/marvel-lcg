"""Le plafond des capacites nommees du pilote d'autoplay.

Usage: python3.10 tools/test_autoplay_plafond.py

⚠ POURQUOI CE FICHIER EXISTE. Mesure du 15/09/2026 sur `iron_patriot` :
l'Action « Enlistment » de `ip002a` etait prise 21 FOIS dans le seul round 1,
20 allies REGISTERED entraient en jeu, et la partie se perdait au round 1 sans
que le pack ait ete exerce. La gate la plus chere du projet etait aveugle sur
ce pack.

⚠ ET IL NE MONTE PAS LE MOTEUR. `autoplay.py` n'importe `engine` que DANS ses
fonctions : la regle du plafond se lit donc sans partie, en une seconde. C'est
ce qui permet de la garder par un cas plutot que par une fournee de 16 parties.
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from autoplay import (ACTES_DE_BASE, PLAFOND_CAPACITE_NOMMEE,  # noqa: E402
                      est_capacite_nommee)

echecs = []


def verifier(condition, message):
    if not condition:
        echecs.append(message)


# --- ce qui est une action de BASE, et n'est jamais plafonne ---------------
#
# Attaquer trois fois avec trois allies differents est normal ; reprendre trois
# fois la meme Action nommee ne l'est pas.
for nom in ("Attack", "Thwart", "Defense", "Recover", "Play", "Change_Form",
            "End Phase", "Resolve Mulligans"):
    verifier(not est_capacite_nommee(nom),
             f"« {nom} » est une action de base : elle ne doit jamais etre plafonnee")

# Le journal du pilote detaille le type joue (« Play:Ally », « Play:Event ») :
# ces entrees comptent des cartes jouees, pas une capacite reprise.
for nom in ("Play:Ally", "Play:Event", "Play:Upgrade"):
    verifier(not est_capacite_nommee(nom),
             f"« {nom} » est une carte jouee, pas une capacite nommee")

# Les formes multiples (Quicksilver, Wasp...) passent par « Change_To_<nom> ».
verifier(not est_capacite_nommee("Change_To_Giant"),
         "un changement de forme reste une action de base")

# Epuiser l'identite a sa propre branche dans le scorer.
verifier(not est_capacite_nommee("exhaust_identity"),
         "epuiser l'identite est traite a part par le scorer")

# --- ce qui EST une capacite nommee ---------------------------------------
for nom in ("Enlistment", "Alter-Ego_Action", "Hero_Action", "Spider-Sense",
            "Minion_Activates_Order"):
    verifier(est_capacite_nommee(nom),
             f"« {nom} » est une capacite nommee : elle doit etre plafonnee")

# ⚠ LE CAS QUI COMPTE : c'est celui-la qui a ete mesure a 21 reprises.
verifier(est_capacite_nommee("Enlistment"),
         "« Enlistment » DOIT etre plafonnee : 21 reprises mesurees au round 1")

# --- le plafond lui-meme ---------------------------------------------------
#
# Mesure du 15/09/2026, 4 parties par valeur, iron_patriot contre Rhino :
#   plafond 1 -> 1,2 rounds tenus ; plafond 2 -> 1,2 ; plafond 3 -> 1,5.
# Serrer davantage ne rend pas le pilote meilleur, il le rend plus pauvre.
verifier(PLAFOND_CAPACITE_NOMMEE == 3,
         f"le plafond mesure vaut 3, pas {PLAFOND_CAPACITE_NOMMEE} : "
         "1 et 2 ont ete mesures PIRES (1,2 rounds contre 1,5)")

# Un garde-fou sur la liste elle-meme : un nom retire par megarde rendrait une
# action de base plafonnable, et le pilote cesserait d'attaquer apres trois
# coups.
verifier("Attack" in ACTES_DE_BASE and "Thwart" in ACTES_DE_BASE,
         "Attack et Thwart doivent rester dans ACTES_DE_BASE")

if echecs:
    print(f"ECHEC : {len(echecs)} cas")
    for e in echecs:
        print(f"  - {e}")
    sys.exit(1)
print("OK : le plafond des capacites nommees tient (11 cas)")
