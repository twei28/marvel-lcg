from . import *


def GetAbilities() -> Sequence['Ability']:
    def with_great_firepower(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        effect.GetInitiator().PlayCardsLikeInTurn(effect.targets, effect, update_resources_cost=-2)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            for_card=CardFinder(card_type=Upgrade),
            is_play_card=False,                    # « for an upgrade ABILITY » : pas pour JOUER une amelioration
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            with_great_firepower,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(card_type=Upgrade, traits=["WEAPON", "TECH"], canbe_play=True, from_where=["YourHandCards"]),
    ]
