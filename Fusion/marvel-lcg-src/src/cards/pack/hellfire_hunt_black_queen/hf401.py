from . import *

# Selene (stade I). « Forced Response : After Selene attacks, heal damage from her equal to the amount of non-excess damage characters the defending
# player controlled took from this attack. » 
# Carte de reference : `VolDeVie` (__init__.py) = `AfterUnitAttackEnd(ForcedResponse, "This")` + `HealHealth`. Aucun mot-cle a recoder.


def GetAbilities() -> Sequence['Ability']:
    return [VolDeVie()]
