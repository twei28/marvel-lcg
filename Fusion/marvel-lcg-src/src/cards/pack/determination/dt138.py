from . import *

# Assessed for Weakness

def GetAbilities() -> Sequence['Ability']:

    def assessed_for_weakness(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        if initiator.AskChooseOneText(["+1", "-1"]) == "+1":
            message.IncreaseDamage(1, effect)
        else:
            message.PreventDamage(1, effect)

    def check_attache(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Upgrade)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion)
        ),
        # « le sbire attache gagne fragile » : Fragile() cible "This", ici c'est
        # le sbire porteur, d'ou la fenetre ecrite en clair.
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            None,
            "AttachedMinion",
            lambda effect, message: message.GainOverKill(effect),
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            None,
            assessed_for_weakness,
            conditions=[check_attache],
        ),
    ]
