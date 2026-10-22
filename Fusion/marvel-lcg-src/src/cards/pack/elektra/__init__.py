from cards.pack import *
from cards.pack.fne import DiscountAbility

# ===========================================================================
# Pack officiel ELEKTRA NATCHIOS (Hero Pack MC63, Fantasy Flight Games, sortie annoncee en novembre 2026) :
# CARTES D'ASPECT SEULEMENT (Aggression, Basic, Justice, Leadership, Protection, n° de collection 15-39), ajoutees le
# 22/10/2026 depuis les scans Hall of Heroes (page + captures « content creator »). Perimetre decide par l'utilisateur :
# PAS le heros Elektra ni ses cartes signature. Ces cartes sont OFFICIELLES (pas de champ `custom`, pas de prefixe lettre).
# Numerotation = numero de collection imprime (63015-63039). Scripts a la RACINE du pack, `set_name` vide.
# Sources : .planning/elektra-officiel/. Gabarits PROCESSUS-CARTE : docs/packs/elektra_cartes.md.
# Cas test_capacites : tools/cas/elektra_aspects.py (noms prefixes « [el_aspect] »).
# ===========================================================================


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (meme helper que le pack iron_fist)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None
