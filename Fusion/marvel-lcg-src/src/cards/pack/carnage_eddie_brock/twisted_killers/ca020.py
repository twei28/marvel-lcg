from . import *

# * Bushwacker : SBIRE (BRUTE. KILLER.), SCH 1, ATK 2 (consecutif), PV 8, boost 2. Set modulaire « Twisted Killers ».
# Toughness. Villainous.
# [star] Bushwacker's attacks gain piercing and overkill.
# [star] Boost: If Murderous Nature is attached to this enemy, give this enemy another boost card.
#
# CARTES DE REFERENCE
#  - Toughness / Villainous : natifs (`desc`, fiches toughness.md / villainous.md), aucun code.
#  - « X's attacks gain piercing and overkill » : `UnitAttackGainKeyword("This", piercing=True, overkill=True)` (do_attack.py:828, modele ca006 / im012 ; fiches piercing.md, overkill.md).
#  - Boost etoile « give this enemy another boost card » : `27141` / `sender_card.py` : `message.GiveActivatingEnemyAdditionalBoostCard(1, effect)` ; test « attache a cet ennemi » sur les attachements de l'ennemi qui s'active.
#
# TEXTE CONTRE CODE
#  « Bushwacker's ATTACKS gain piercing AND overkill » : toutes ses attaques, les deux mots-cles. « [star] Boost: IF Murderous Nature is attached TO THIS ENEMY » : lecon du boost : « this enemy » = l'ennemi qui s'active et recoit cette carte de boost (pas Bushwacker, qui n'est qu'une carte retournee) ;
#    une seule carte de boost supplementaire, seulement si Murderous Nature est attachee a cet ennemi. Chiffres : PV 8, ATK 2, SCH 1, boost 2.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        activant = message.activating_enemy
        if activant is None:
            return
        if any(a.IsName(NOM_MURDEROUS_NATURE) for a in activant.GetAttachedAttachments()):
            message.GiveActivatingEnemyAdditionalBoostCard(1, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            overkill=True,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
