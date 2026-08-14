from . import *

# Shocked

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Discard cards from the top of the encounter deck
        # equal to the number of cards in your hand. If 3 or fewer cards were
        # discarded this way, this card gains surge. »
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        combien = len(joueur.hand_cards.Get())
        defaussees = Worlds.DiscardEncounterCards(combien, effect) if combien > 0 else []
        if len(defaussees) <= 3:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
