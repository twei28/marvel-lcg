from cards.pack import *

# ===========================================================================
# Pack officiel IRON FIST (Hero Pack MC64EN, Fantasy Flight Games, sortie
# annoncee en novembre 2026). Set « Iron Fist » : 64001a/64001b (Iron Fist /
# Danny Rand) et les 11 cartes signature 64002-64012 (15 exemplaires).
#
# Perimetre decide par l'utilisateur le 20/10/2026 : heros + cartes signature
# seulement (pas les cartes d'aspect du pack, pas les cartes de rencontre :
# rien n'est publie). Sources : .planning/iron-fist-officiel/ (releve
# Hall of Heroes, lecture, cinq decisions de l'utilisateur, questions).
# Gabarits PROCESSUS-CARTE : docs/packs/iron_fist_cartes.md.
# Cas test_capacites : tools/cas/iron_fist.py (noms prefixes « [iron_fist] »).
# ===========================================================================

# ===========================================================================
# CARTES D'ASPECT du pack (Protection / Basic / Aggression / Leadership, 64013-64033), ajoutees le
# 22/10/2026 depuis les scans Hall of Heroes (page + captures « content creator »). Elles n'ont pas de
# `set_name` : leur script vit ICI, a la racine du pack (comme `luke_cage/62012.py`), pas dans le dossier du
# set signature. Gabarits : docs/packs/iron_fist_cartes.md. Plan : .planning/iron-fist-officiel/aspects-plan.md.
# ===========================================================================
from cards.pack.fne import DiscountAbility


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (meme helper que le set signature)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None
