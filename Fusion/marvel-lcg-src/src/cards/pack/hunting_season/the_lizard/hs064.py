from . import *

# Komodo Claws

def GetAbilities() -> Sequence['Ability']:
    return [
        AttacherAuLizard(),
        *AbilityFactory.GiveKeywordToAttached(retaliate=1),
        ActionHeros(Cost("Y"), CostFunc.TakeDamage(1, "YourIdentity")),
    ]
