from . import *

# Path of Penance

def GetAbilities() -> Sequence['Ability']:

    def path_of_penance(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        surplus = message.excess_damage
        if player is None or surplus <= 0:
            return
        hero = player.GetHero()
        avant = hero.health
        this.DealDamage([hero], surplus, effect)
        pris = avant - hero.health

        for _ in range(pris):
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Choose a player to draw 1 card",
                    lambda targets:
                        [p.DrawUp(1, effect) for p in Worlds.GetPlayers(effect)][:1]
                ).SetHasNoTargetEffect()
            )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            "You",
            Minion,
            path_of_penance,
        ).LimitOncePerRound(),
    ]
