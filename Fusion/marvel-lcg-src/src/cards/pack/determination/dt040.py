from . import *

# Suckerpunch

def GetAbilities() -> Sequence['Ability']:

    def suckerpunch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 2, effect)
        PeutRevenirEnMain(this, initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            suckerpunch
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
