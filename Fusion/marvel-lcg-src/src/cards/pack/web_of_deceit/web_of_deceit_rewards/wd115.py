from . import *

# Great Web Warrior

def GetAbilities() -> Sequence['Ability']:

    return [
        # « You gain the WEB-WARRIOR trait. You get +2 hit points. »
        #
        # ⚠ Rend une LISTE d'abilites : l'etoile n'est pas optionnelle.
        *AbilityFactory.GiveKeywordToAttached(
            trait="WEB-WARRIOR",
            health=2,
        ),
    ]
