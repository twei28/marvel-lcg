from . import *

# Target Painted

def GetAbilities() -> Sequence['Ability']:

    def target_painted(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)

        sbire = this.GetBindFace()
        if sbire is None or message.target is not sbire:
            return
        message.GainRanged(effect)
        supplement = len(sbire.GetInventoryDeck().GetAll())
        if supplement:
            message.would_atk_message.GainATKForThisAttack(supplement, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion)
        ).SetPlay(only_if_your_identity_has_trait="SOLDIER"),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            None,
            "AttachedMinion",
            target_painted,
        ),
    ]
