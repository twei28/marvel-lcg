from . import *

# Last Laugh

def GetAbilities() -> Sequence['Ability']:

    def check_half_hp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        hero = effect.GetInitiator().GetHero()
        return hero.health < hero.starting_health/2

    def last_laugh(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        initiator.GetHero().TakeDamage(this, 1, effect)

        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 6, effect)

        initiator.GetIdentity().ChangeToOtherForm(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            last_laugh,
            conditions=[check_half_hp],
        ).SetPlay().SetLabel('attack'),
    ]
