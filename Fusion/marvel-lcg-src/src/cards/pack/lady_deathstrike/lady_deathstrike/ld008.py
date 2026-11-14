from . import *

# Reinforced Adamantium Claws — ATTACHEMENT, WEAPON. ATK +1[star]. Boost : etoile seule.
# Attach to Lady Deathstrike.
# [star] Lady Deathstrike's attacks gain piercing.
# Hero Response: After you attack Lady Deathstrike, resolve the "Special" ability on the copy of Bleeding Out attached to your identity
#   → discard this card.
# [star] Boost: Reveal this card.
#
# Cartes de reference :
#  - `40090` Heavy Armament : `AfterUnitAttackUnit(HeroResponse, "You", "AttachedEnemy", DiscardThisCard)` + cout ; `ATK+` natif de `desc`.
#  - « gain piercing » : `UnitAttackGainKeyword("AttachedEnemy", piercing=True)` (fiche mots-cles/piercing.md) ;
#  - cout = resoudre le Special : `CostFunc.Custom(None, fn)` (`40092` Inhibitor Collar) ; `ld007` pour le Boost « Reveal ».
#
# ⚠ Mots-pieges :
#  - « → » : ce qui precede est le COUT : le joueur DOIT pouvoir resoudre son Special (toujours possible), puis la carte est defaussee ;
#  - « After YOU attack » : le heros du joueur (Hero Response), pas un allie ;
#  - `ATK+` « 1* » : +1 ATK a l'ennemi porteur (lu dans desc), l'etoile renvoie au piercing du texte ;
#  - si ld002 ne trouve pas les Griffes (deja en jeu), elles ne sont pas re-revelees.


def GetAbilities() -> Sequence['Ability']:

    def saigner_en_cout(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        ResoudreSaignement(effect, effect.GetInitiator())
        return True

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=IDS_VILAIN)),
        AbilityFactory.UnitAttackGainKeyword("AttachedEnemy", piercing=True),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            "You",
            "AttachedEnemy",
            DiscardThisCard,
        ).SetCostFunc(CostFunc.Custom(None, saigner_en_cout)),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
