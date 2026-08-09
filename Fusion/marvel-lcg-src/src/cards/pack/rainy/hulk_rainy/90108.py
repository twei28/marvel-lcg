from . import *

# Natural Genius

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CheckThisCanDropPay(
            Resources("BB"),
            spend_this_only_in_alter_ego_form=True
        )
    ]
