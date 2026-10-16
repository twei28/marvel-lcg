from . import *

# Bladed Armor — ATTACHEMENT. ARMOR. FOOT CLAN. RELIC. ATQ +1, 3 icones de boost.
# Attach to Shredder.
# Shredder gains Retaliate 1.
# Hero Action: If there are no cloaked status cards on Shredder, take 1 damage
#   and spend 1 resource of any type -> discard this card.
#
# Cartes de reference :
#  - `01100` Enhanced Ivory Horn : `AttachToFaceWhenPutIntoPlay` +
#    `PlayerActionToDiscardThis(HeroAction)` (« Spend ... -> discard this card ») ;
#  - `gmw 16097` Weapon Mastery : `*GiveKeywordToAttached(CardFinder, retaliate=1)` ;
#  - `bl009` Daywalker : `CostFunc.TakeDamage(1, "YourIdentity")` pour « take 1
#    damage -> » ; `gmw` Element Gun / `sm 27130` : `Cost("1")` = « spend 1
#    resource of any type ».
#
# Mots-pieges : « IF there are NO cloaked status cards on Shredder » = condition
# pour OFFRIR l'action (Shredder porte 0 Cloaked) ; « take 1 damage » et « spend
# 1 resource » sont deux COUTS (avant le « -> ») ; « Shredder » retrouve par
# card_id (`IDS_SHREDDER`).
#
# DECISION UTILISATEUR (16/10/2026, Q1) : « take 1 damage »
# sans sujet. Lecture retenue : l'IDENTITE du joueur qui paie prend 1 degat.


def GetAbilities() -> Sequence['Ability']:

    def pas_de_cloaked(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        shredder = TrouverShredder(effect)
        return shredder is not None and not shredder.IsCloaked()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=IDS_SHREDDER)),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(card_ids=IDS_SHREDDER), retaliate=1),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            conditions=[pas_de_cloaked],
        ).SetCost(Cost("1")).SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity")),
    ]
