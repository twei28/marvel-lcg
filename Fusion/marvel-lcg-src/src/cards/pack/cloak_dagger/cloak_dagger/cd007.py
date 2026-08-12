from . import *

# Lightforce Absorption — custom « DesignHacker »
# Response: After you play a LIGHTFORCE card, exhaust Lightforce Absorption →
#   shuffle a LIGHTFORCE card from your discard pile into your deck.
# (Texte d'origine : « from Dagger's discard pile into Dagger's deck » ; avec
#  un seul deck, c'est le vôtre. Écart §9.)


def GetAbilities() -> Sequence['Ability']:

    def lightforce_absorption(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=False,
            include_discard_pile=True,
            not_move=True,
            trait="LIGHTFORCE",
        )
        if face:
            Faces.ShuffleAllTo([face], initiator.player_deck, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(traits=["LIGHTFORCE"]),
            lightforce_absorption,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
