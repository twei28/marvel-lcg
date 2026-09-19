from . import *

# Charging Up (side scheme, 6, alea : base)
# When Defeated: Place 3 charge counters on Electric Charge.

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        PoserCharges(effect, 3)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
