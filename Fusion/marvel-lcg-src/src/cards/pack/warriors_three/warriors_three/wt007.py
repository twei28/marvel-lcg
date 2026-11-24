from . import *


def GetAbilities() -> Sequence['Ability']:
    def soin(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        effect.this.HealthUnits([message.trigger], 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Volstagg"), attack=1, retaliate=1),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            soin,
            conditions=[lambda effect, message: message.trigger.IsName("Volstagg")],
        ),
    ]
