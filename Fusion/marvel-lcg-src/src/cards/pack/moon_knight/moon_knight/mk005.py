from . import *

# Different Folks — custom « DesignHacker »
# After you change form, place a madness counter here.
# Hero Action: Remove 6 madness counters from Different Folks → stun an enemy.


def GetAbilities() -> Sequence['Ability']:

    def compter(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.PlaceCountersOn([this], 1, 'madness', effect)

    def stun(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "You",
            compter,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stun,
        ).SetName("Different Folks")
        .SetCostFunc(CostFunc.Counter("This", 6, 'madness'))
        .SetTarget(Enemy, canbe_stunned=True),
    ]
