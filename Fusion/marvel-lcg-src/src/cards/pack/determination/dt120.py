from . import *

# Jury Rigged Tech

def GetAbilities() -> Sequence['Ability']:

    def jury_rigged_tech(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        carte_boost = message.trigger.CastTo(HasBoostIcon)
        x = carte_boost.boost_icon + carte_boost.boost_star

        dessus = initiator.DiscardDeckTopCard(effect)
        if dessus is None or dessus.printed_cost <= x:
            return
        # « all-purpose counter » : le moteur le connait sous le nom `counter`,
        # et `GetCounters('all-purpose')` en rend le total.
        for _ in range(x):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Place an all-purpose counter on a card you control",
                    lambda targets: Faces.PlaceCountersOn(targets, 1, 'counter', effect)
                ).SetTarget("YouControlCards")
            )
        Faces.DiscardAll([message.trigger], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenCardBecomeBoost(
            None,
            jury_rigged_tech
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
