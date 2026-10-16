from cards.pack import *

# ===========================================================================
# Set nemesis « Raphael Nemesis » (Old Hob, Inkwire, prefixe `tr`).
# `tr015` Old Hob n'a aucun script : Toughness,
# Quickstrike et Nemesis sont des BASES AUTOMATIQUES lues dans `desc`.
#
# ⚠ L'obligation `tr013` Out of Control a le bandeau « RAPHAEL », pas
# « RAPHAEL NEMESIS » : son module vit dans `raphael/raphael/`.
# ===========================================================================


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (modele sunfire).

    ⚠ Une carte de RENCONTRE n'appartient a aucun joueur : passer le joueur
    EXPLICITEMENT (`message.GetToPlayer()`) pour les traitrises, comme
    `mw020`, `rg017`, `57062`.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def DefausserUneCarteDeLaMain(joueur: 'Player', effect: 'Effect') -> bool:
    """« Discard 1 card from your hand. » — le JOUEUR choisit (pas au hasard).

    Modele `57062` (boost « Discard 1 card from your hand »). Rend True si une
    carte a ete defaussee, False si la main est vide.
    """
    main = list(joueur.hand_cards.Get())
    if not main:
        return False

    def defausser(choisies: Sequence['CardFace']) -> None:
        Faces.DiscardAll(list(choisies), effect)

    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Discard 1 card from your hand",
            defausser,
        ).SetTarget(main, range=(1, 1), not_move=True),
    )
    return True
