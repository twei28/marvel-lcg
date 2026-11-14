from . import *

# Cloaking Device — ATTACHEMENT. WEAPON. Boost 1.
# Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge.
# Reduce the amount of damage attached enemy takes from each attack by 2.
# Hero Action: After a hero makes a basic attack against this enemy, spend [energy][physical] resources → discard this card.
#
# Cartes de reference : 21117 (Thanos) : `ReduceCharacterTakeDamageBy(.., from_each_attack=True)` + `AfterUnitMakeBasicAttack(HeroResponse,
#   Hero, DiscardThisCard, against_who=).SetCost(Cost("YR"))` ; attachement : `AttacherAuWarlordSinonYautja` (comme ap012).
#
# ⚠ Mots-pieges :
#  - « Hero Action: After ... » : formulation hybride ; arbitrage 3 du 25/10/2026 : c'est une REPONSE de heros, juste apres l'attaque de
#    base contre l'ennemi equipe ;
#  - « from EACH attack » : -2 par attaque (pas par source de degats) ; [energy] = Y, [physical] = R.


def GetAbilities() -> Sequence['Ability']:
    return [
        AttacherAuWarlordSinonYautja(),
        AbilityFactory.ReduceCharacterTakeDamageBy("AttachedEnemy", 2, this_attached_unit_only=True, from_each_attack=True),
        AbilityFactory.AfterUnitMakeBasicAttack(AbilityType.HeroResponse, Hero, DiscardThisCard,
                                                against_who="AttachedEnemy").SetCost(Cost("YR")),
    ]
