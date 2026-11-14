from . import *


def GetAbilities() -> Sequence['Ability']:
    def soigne(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        effect.this.HealthUnits(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            soigne,
            to_form=AlterEgo,
        ).SetTarget(
            check_fn=lambda effect, face: Identity.IsType(face) or Ally.IsType(face),
            from_where=["YouControlCards"],
        ),
    ]
