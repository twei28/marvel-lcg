from . import *

# * Spider-Man (Ben Reilly) — custom « Rainy »
# [star] Interrupt: When this ally uses a basic power, web an enemy
#   (maximum 3 web counters per enemy).

def GetAbilities() -> Sequence['Ability']:

    def toile(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        Weber(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            toile,
            is_basic_attack=True,
        ).SetTarget(Enemy).SetName("Web an enemy"),

        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.Interrupt,
            "This",
            toile,
            is_basic_thwart=True,
        ).SetTarget(Enemy).SetName("Web an enemy"),
    ]
