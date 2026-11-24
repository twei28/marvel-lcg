from . import *

# Shining Shield (x2). Attachement PSIONIC SKILL. « Attach to Selene. Selene cannot take more than 2 damage from a single attack. Hero Action :
# Spend a [energy] resource and remove 1 time counter from Beneath the Sun -> discard this card. [star] Boost : Attach this card to Selene. »
# Cartes de reference : 40091 Titanium Exoskeleton (`UnitCannotTakeDamageWhile(..., "AttachedEnemy", cannot_take_more_than_damage=2,
# is_from_attack=True)`), `WhenThisBoostAttachTo` (asset.py:204), hf413 (cout en compteur de temps).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(ChercheurSelene()),
        AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, "AttachedEnemy", cannot_take_more_than_damage=2, is_from_attack=True),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("Y")).SetCostFunc(CoutTempsDuJour()),
        AbilityFactory.WhenThisBoostAttachTo(ChercheurSelene()),
    ]
