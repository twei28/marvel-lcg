from . import *

# Web-Warriors

def GetAbilities() -> Sequence['Ability']:

    return [
        # « Each of your WEB-WARRIOR allies gets +1 hit point and +1 ATK. »
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="WEB-WARRIOR", card_type=Ally),
            control_by="You",
            health=1,
            attack=1,
        ),
    ]
