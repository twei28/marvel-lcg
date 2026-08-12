from . import *

# * Flash Thompson — custom « DesignHacker »
# Boy Scout — Response: After you change to this form, heal 2 damage from any
#   character.

def GetAbilities() -> Sequence['Ability']:

    def boy_scout(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        this.HealthUnits(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            boy_scout,
            to_this_form=True,
        ).SetName("Boy Scout")
        .SetTarget(Unit2, canbe_heal=True),
    ]
