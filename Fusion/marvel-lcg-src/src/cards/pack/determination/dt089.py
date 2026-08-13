from . import *

# Concatenate

def GetAbilities() -> Sequence['Ability']:

    def concatenate(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)

        ennemi = message.target
        tactiques = [f for f in ennemi.GetInventoryDeck().GetAll()
                     if Upgrade.IsType(f) and f.HasTrait("TACTIC")]
        if not tactiques:
            return
        Faces.DiscardAll(tactiques, effect)
        this.DealDamage([ennemi], 2 * len(tactiques), effect)
        message.GainOverKill(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Enemy)
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.HeroInterrupt,
            "You",
            "AttachedEnemy",
            concatenate,
        ).SetLabel('attack'),
    ]
