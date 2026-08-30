from . import *

# Mark of Kaine (2/3) — exemplaire physique 2 de 3, contenu identique a
# ss012 (voir ce fichier pour le detail du modele repris).


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
