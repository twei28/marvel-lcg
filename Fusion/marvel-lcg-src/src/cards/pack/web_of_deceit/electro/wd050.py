from . import *

# Charging

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Discard cards from the top of the encounter deck
        # until a minion is discarded. If that minion is Electro, put it into
        # play and it gains quickstrike. Otherwise, this card gains surge. »
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        sbire = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=Minion,
        )
        if sbire and sbire.IsName("Electro"):
            sbire.PutIntoPlay(joueur, effect)
            sbire.CastTo(Minion).GainKeyword(1, 'Quickstrike', effect)
        else:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
