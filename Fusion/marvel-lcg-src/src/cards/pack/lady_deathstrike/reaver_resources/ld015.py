from . import *

# Integrated Augmentations — ATTACHEMENT (module Reaver Resources). TECH. WEAPON. ATK +1[star]. Boost 2.
# Attach to the enemy with the highest printed ATK.
# Attached enemy gains retaliate 1.
# [star] Attached enemy's attacks gain ranged.
# Hero Response: After you attack the attached enemy, spend [energy][mental] resources → discard this card.
#
# Cartes de reference :
#  - `40090` Heavy Armament (Military Grade) : MEME squelette (`AttachToFaceWhenPutIntoPlay(Enemy, highest_atk=True)`,
#    `GiveKeywordToAttached(Enemy, retaliate=..)`, `AfterUnitAttackUnit(HeroResponse, "You", "AttachedEnemy", DiscardThisCard).SetCost(..)`) ;
#    `32028` Unstoppable pour `highest_printed_atk=True` ; `50107b` M.O.D.O.K. pour `UnitAttackGainKeyword(..., ranged=True)`.
#
# ⚠ Mots-pieges :
#  - « highest PRINTED ATK » : l'ATK IMPRIMEE (`highest_printed_atk`), pas l'ATK courante ; egalite : le moteur depart des cas ex aequo ;
#  - `[energy][mental]` : DEUX types differents, `Cost("YB")` ; « After YOU attack the attached enemy » : le heros ;
#  - ATK+ « 1* » (desc) : +1 ATK a l'ennemi porteur ; l'etoile = les attaques a distance.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Enemy,
            highest_printed_atk=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Enemy,
            retaliate=1,
        ),
        AbilityFactory.UnitAttackGainKeyword("AttachedEnemy", ranged=True),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            "You",
            "AttachedEnemy",
            DiscardThisCard,
        ).SetCost(Cost("YB")),
    ]
