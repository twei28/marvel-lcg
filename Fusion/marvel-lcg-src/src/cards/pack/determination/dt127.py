from . import *

# Collective Breather

def GetAbilities() -> Sequence['Ability']:

    def collective_breather(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        blesses = [x for x in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not x.IsDefeated() and x.CastTo(CanHealth).sustained > 0]
        if not blesses:
            return
        this.HealthUnits(blesses, 2, effect)

        for _ in blesses:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready a friendly character",
                    lambda targets: Faces.ReadyAll(targets, effect)
                ).SetTarget(Friend, canbe_ready=True)
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            collective_breather
        ).SetPlay().LimitOncePerRound(),
    ]
