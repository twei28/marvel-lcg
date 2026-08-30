from . import *

# Mark of Kaine (1/3) — SUPERPOWER
# Attach to a minion. Attacks against this minion gain overkill.
# Hero Interrupt: When Scarlet Spider deals excess damage to this minion,
#   increase that damage by 2.
#
# "Attacks against this minion gain overkill" : modele officiel exact 33032
# Marked (`AbilityFactory.WhenUnitWouldAttackUnit(None, "AttachedMinion",
# marked)` + `message.GainOverKill(effect)`). "Increase that damage by 2" :
# modele gmw/16045.py (Follow Through), `AbilityFactory.
# WhenUnitAttackDealExcessDamage(AbilityType.HeroInterrupt, "You", ...)` +
# `message.IncreaseDamage(2, effect)`, restreint AU SEUL sbire attache via
# `Condition.CheckWhichCard("AttachedMinion", message.target, effect)`
# (meme mot-cle de condition qu'utilise en interne 33032 pour "AttachedMinion").


def GetAbilities() -> Sequence['Ability']:

    def gain_overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainOverKill(effect)

    def increase_excess_damage(effect: 'Effect', message: 'Message.WhenCalcDealExcessDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.IncreaseDamage(2, effect)

    def targets_this_minion(effect: 'Effect', message: 'Message.WhenCalcDealExcessDamage') -> bool:
        return Condition.CheckWhichCard("AttachedMinion", message.target, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Minion),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            None,
            "AttachedMinion",
            gain_overkill,
        ),
        AbilityFactory.WhenUnitAttackDealExcessDamage(
            AbilityType.HeroInterrupt,
            "You",
            increase_excess_damage,
            conditions=[targets_this_minion],
        ),
    ]
