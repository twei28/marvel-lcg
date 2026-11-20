from . import *

# Vibranium Gun — AMELIORATION, cout 2, [mental]. Restricted. TECH. WEAPON. WAKANDA.
# Restricted.
# Roz's basic attacks gain ranged.
# Special (attack): Deal 2 damage to an enemy. This attack gains piercing.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - Special (attack) : `51011` Panther Claws (bp) : `WhenResolveSpecialAbility("This", op).SetLabel('attack')
#    .SetTarget(Enemy)` + `this.DealDamage(effect.targets, N, effect, property=AttackProperty(piercing=...))`.
#  - ranged sur les attaques de BASE d'un personnage : `22004` Cutthroat Ambition
#    (`UnitAttackGainKeyword(CardFinder(name=..., card_type=Hero), ...)`), `is_basic_attack=True`.
#  - Restricted : `desc.Restricted = "1"`, base automatique (fiche mots-cles/restricted.md), rien a coder.
#
# MOTS-PIEGES
#  - « Roz's BASIC attacks gain ranged » : `is_basic_attack=True` (un evenement d'attaque ne gagne pas ranged).
#  - « Deal 2 damage to AN enemy » : vilain ou sbire ; « THIS ATTACK gains piercing » : `AttackProperty(piercing=True)`
#    sur ce Special seulement, pas sur les attaques de base.
#  - le Special est une ATTAQUE (`SetLabel('attack')`) : la Riposte s'applique, mais pas contre un tir ranged.
def GetAbilities() -> Sequence['Ability']:

    def tir(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.DealDamage(effect.targets, 2, effect, property=AttackProperty(piercing=True))

    return [
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name="Roz", card_type=Hero),
            ranged=True,
            is_basic_attack=True,
        ),
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            tir,
        ).SetLabel('attack')
        .SetTarget(Enemy),
    ]
