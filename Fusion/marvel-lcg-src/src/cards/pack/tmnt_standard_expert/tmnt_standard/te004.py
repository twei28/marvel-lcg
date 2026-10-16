from . import *

# Pursued by Shadows (TMNT Standard 4/7) — TRAITRISE. 2 icones de boost.
# When Revealed: Search the encounter deck, discard pile, and set-aside area for
#   your nemesis minion and reveal it. (Shuffle.) Cloak your nemesis minion. If
#   your nemesis minion did not enter play this way, this card gains surge.
#
# Cartes de reference : `hood 24031` Seek and Destroy / `mts 21188` (la recherche
# `Search.EncounterCard(include_discard_pile=True, include_set_aside=True,
# is_nemesis=player)`), `01190` Shadow of the Past (`Reveal(..., if_entered_play=)`
# + `ThisCardGainSurge`).
#
# Mots-pieges : « YOUR nemesis minion » (`is_nemesis=player`, jamais celui d'un
# autre joueur) ; « Cloak your nemesis minion » : meme s'il etait DEJA en jeu ;
# « did not enter play THIS WAY » : seule la revelation de cette carte compte.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        entre = False

        def marquer() -> None:
            nonlocal entre
            entre = True

        sbire = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            include_set_aside=True,
            card_type=Minion,
            is_nemesis=joueur,
        )
        if sbire:
            sbire.Reveal(joueur, effect, if_entered_play=marquer)
        Cloak(effect, Worlds.FindCardOnField(effect, card_type=Minion, is_nemesis=joueur))
        if not entre:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
