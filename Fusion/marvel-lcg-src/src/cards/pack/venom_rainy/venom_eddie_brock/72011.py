from . import *

# Sharp Teeth — custom « Rainy »
# Venom gets +1 ATK. Venom's basic attacks gain overkill and piercing.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            attack=1,
        ),

        AbilityFactory.UnitAttackGainKeyword(
            "You",
            overkill=True,
            piercing=True,
            is_basic_attack=True,
        ),
    ]
