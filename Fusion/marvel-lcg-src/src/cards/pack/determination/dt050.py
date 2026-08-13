from . import *

# Glutton for Punishment

def GetAbilities() -> Sequence['Ability']:

    def check_half_hp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        hero = effect.GetInitiator().GetHero()
        return hero.health < hero.starting_health/2

    def glutton_for_punishment(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 8, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            glutton_for_punishment,
            conditions=[check_half_hp],
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.TakeDamage(2, "Initiator")),
    ]
