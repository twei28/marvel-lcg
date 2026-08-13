from . import *

# Explosives Training

def GetAbilities() -> Sequence['Ability']:

    def explosives_training(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Support)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(
        ).SetPlay(only_if_your_identity_has_trait="GUARDIAN"),
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            CardFinder(card_type=Upgrade),
            explosives_training,
            control_by_player="You",
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
