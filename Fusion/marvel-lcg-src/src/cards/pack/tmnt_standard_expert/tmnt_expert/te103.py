from . import *

# Sinister Plan (TMNT Expert 3/3) — TRAITRISE. 3 icones de boost.
# When Revealed: Search the encounter deck, discard pile, and set-aside area for
#   your nemesis side scheme and reveal it. (Shuffle.) Daze your identity. If your
#   nemesis side scheme did not enter play this way, this card gains surge.
#
# Cartes de reference : `te004` (recherche + `if_entered_play`), `te001` (`Daze`).
#
# Mots-pieges : « YOUR nemesis SIDE SCHEME » (type SchemeSide2, `is_nemesis`) ;
# on dazes TOUJOURS ; le surge seulement si le complot annexe n'est pas entre.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        entre = False

        def marquer() -> None:
            nonlocal entre
            entre = True

        complot = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            include_set_aside=True,
            card_type=SchemeSide2,
            is_nemesis=joueur,
        )
        if complot:
            complot.Reveal(joueur, effect, if_entered_play=marquer)
        Daze(effect, joueur.GetIdentity())
        if not entre:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
