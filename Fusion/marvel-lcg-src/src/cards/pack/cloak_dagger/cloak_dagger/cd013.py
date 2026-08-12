from . import *

# Darkforce Absorption — custom « DesignHacker »
# Response: After you play a DARKFORCE card, exhaust Darkforce Absorption →
#   shuffle a DARKFORCE card from your discard pile into your deck.
# Miroir exact de Lightforce Absorption (cd007).


def GetAbilities() -> Sequence['Ability']:

    def darkforce_absorption(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=False,
            include_discard_pile=True,
            not_move=True,
            trait="DARKFORCE",
        )
        if face:
            Faces.ShuffleAllTo([face], initiator.player_deck, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(traits=["DARKFORCE"]),
            darkforce_absorption,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
