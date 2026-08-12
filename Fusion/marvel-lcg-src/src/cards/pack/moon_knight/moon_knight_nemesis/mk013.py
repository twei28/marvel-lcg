from . import *

# * Bushman — custom « DesignHacker » (némésis de Moon Knight)
# Forced Interrupt: When Bushman would be defeated, if there is no madness
#   counter here, heal all damage from Bushman and put a madness counter on
#   him instead.
# [star] Bushman gets +2 ATK if there is a madness counter here.


def GetAbilities() -> Sequence['Ability']:

    def survit(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        this.HealthUnits([this], "All", effect)
        Faces.PlaceCountersOn([this], 1, 'madness', effect)

    def sans_compteur(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        this = effect.this.CastTo(Minion)
        return this.GetCounters('madness') == 0

    def avec_compteur(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Minion)
        return 1 if this.GetCounters('madness') > 0 else 0

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            survit,
            conditions=[sans_compteur],
        ),
        AbilityFactory.ThisGainKeyword(
            avec_compteur,
            attack=2,
            change_on_event=OnEvent.Counter("This", 'madness'),
        ),
    ]
