from . import *

# * Yautja Wrist Blades — ATTACHEMENT unique. WEAPON. ATK +2. Boost 2.
# Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge.
# [star] Attached enemy's attacks gain piercing.
# Hero Action: Spend [energy][physical] resources → discard this card.
#
# Cartes de reference :
#  - « Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge. » :
#    `AttachToFaceWhenPutIntoPlay(CardFinder(name=WARLORD), if_cannot_attach_to=Select.From(sbire YAUTJA), if_cannot_gain_surge=True)` ;
#  - ATK +2 : `desc.ATK+`, natif (01100) ; « attacks gain piercing » : `UnitAttackGainKeyword("AttachedEnemy", piercing=True)` (27059) ;
#  - « Hero Action: Spend ... → discard this card » : `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("YR"))` (01119 Klaw).
#
# ⚠ Mots-pieges :
#  - [energy] = Y, [physical] = R (verifie contre les icones des cartes Y/R du core) ;
#  - « attached ENEMY » : le Warlord OU le sbire YAUTJA qui la porte ; unique (✦) : nom « * », natif.


def GetAbilities() -> Sequence['Ability']:
    return [
        AttacherAuWarlordSinonYautja(),
        AbilityFactory.UnitAttackGainKeyword("AttachedEnemy", piercing=True),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("YR")),
    ]
