from . import *

# Unnatural Strength

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CheckThisCanDropPay(
            Resources("RR"),
            spend_this_only_in_hero_form=True
        )
    ]
