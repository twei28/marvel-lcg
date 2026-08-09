from . import *

# * Johnny Storm — custom « DesignHacker »
# Ignition — Action: Exhaust Johnny Storm -> search the top 4 cards of your
# deck for a FIRE card and add it to your hand. If no cards were added to
# your hand this way, ready Johnny Storm. (Limit once per round.)

def GetAbilities() -> Sequence['Ability']:

    def ignition(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)

        initiator = effect.GetInitiator()

        face = Search.PlayerDeckTop(
            effect,
            initiator,
            4,
            trait="FIRE",
        )
        if face:
            initiator.GainCard(face, effect)
        else:
            Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            ignition
        ).SetName("Ignition")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .LimitOncePerRound(),
    ]
