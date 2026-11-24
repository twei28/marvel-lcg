from . import *

# Hobgoblin (pu071a) : voir __init__.py (Pumpkin Bomb) ; Steady : natif (desc).
# ★ Hobgoblin's attacks gain ranged.
# ★ Forced Response : After Hobgoblin attacks you, resolve the "Pumpkin Bomb" ability.
#
# Cartes de reference : `ts201` (`UnitAttackGainKeyword("This", ...)`), jigsaw/pu056a.py (`AfterUnitAttackUnit`
# ForcedResponse "This"/"You").

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        ResoudrePumpkinBomb(effect, message.GetToPlayer(), 1)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", ranged=True),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", "You", apres_attaque),
    ]
