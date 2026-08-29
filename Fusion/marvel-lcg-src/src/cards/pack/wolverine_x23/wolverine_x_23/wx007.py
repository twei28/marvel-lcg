from . import *

# Sisterly Bond
# Hero Interrupt: When Honey Badger thwarts or attacks, add Wolverine's
#   matching power to Honey Badger's power for this use.
#
# Copie de Sisterly Bond (43007). Le declencheur (Honey Badger) et la source
# de puissance (Wolverine) sont tous deux bornes au controleur.


def GetAbilities() -> Sequence['Ability']:

    def sisterly_bond(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        for face in effect.targets:
            message.AddMatchingPowerToThisPerformance(face, effect)

    return [
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.HeroInterrupt,
            CardFinder(name=NOM_SOEUR, check_effect_fn=EstTonHeros),
            sisterly_bond
        ).SetPlay().SetLabel()
        .SetTarget("YourIdentity"),
    ]
