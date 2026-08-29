from cards.pack import *

# ===========================================================================
# Pack RED GUARDIAN — contenu custom de Kajislav, reproduit a l'identique.
#
# Tout le set tourne autour d'UNE carte : « Red Guardian's Shield » (rg008),
# une amelioration unique, sans cout, Temporary, qui n'est jamais jouee
# normalement — elle est ATTACHEE a un ennemi ou a une manigance par la
# capacite « Shield Launch » du heros.
#
# Le bouclier vit dans trois etats, et c'est ce qui structure le pack :
#
#   EN MAIN     -> debloque Shield Block (rg004), Shielded Drop (rg005),
#                  Shield Strike (rg007) ; en contrepartie il occupe une
#                  place de carte restreinte.
#   ATTACHE     -> debloque Black Widow (rg002), White Widow (rg003),
#                  Shield Ricochet (rg006), Shield Arts (rg009).
#   PERDU       -> Shield Harness (rg010) et l'alter-ego (rg001b) le
#                  ramenent.
#
# Les helpers ci-dessous sont le seul endroit qui sait retrouver le bouclier ;
# toutes les cartes passent par eux.
# ===========================================================================

NOM_BOUCLIER = "Red Guardian's Shield"


def BouclierEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Le bouclier s'il est EN JEU (donc attache a une cible), sinon None."""
    return Worlds.FindCardOnField(effect, name=NOM_BOUCLIER)


def CibleDuBouclier(effect: 'Effect') -> 'CardFace|None':
    """L'ennemi ou la manigance qui porte le bouclier, sinon None."""
    bouclier = BouclierEnJeu(effect)
    if bouclier is None:
        return None
    # `bind_face` directement : GetBindFace() leve une assertion si la carte
    # n'est attachee a rien, ce qui arrive entre la mise en jeu et l'attache.
    return bouclier.bind_face


def BouclierEnMain(joueur: 'Player|None') -> 'CardFace|None':
    """Le bouclier s'il est dans la main de ce joueur, sinon None."""
    if joueur is None:
        return None
    for face in joueur.hand_cards.Get():
        if face is not None and face.IsName(NOM_BOUCLIER):
            return face
    return None


def BouclierEstEnMain(effect: 'Effect', message=None) -> bool:
    """Condition « Play only if Red Guardian's Shield is in your hand. »"""
    return BouclierEnMain(effect.GetInitiator()) is not None


def BouclierEstAttache(effect: 'Effect', message=None) -> bool:
    """Condition « Play only if Red Guardian's Shield is attached to an enemy
    or a scheme. »"""
    return CibleDuBouclier(effect) is not None


def RendreLeBouclier(effect: 'Effect', joueur: 'Player|None' = None) -> bool:
    """Ramene le bouclier du JEU vers la main de son proprietaire.

    Sert a trois cartes qui le formulent differemment mais font la meme
    chose : le bouclier lui-meme en fin de tour (rg008), Shield Arts (rg009)
    et Shield Harness (rg010).
    """
    bouclier = BouclierEnJeu(effect)
    if bouclier is None:
        return False
    Faces.ReturnToHand([bouclier], joueur or "Owner", effect)
    return True
