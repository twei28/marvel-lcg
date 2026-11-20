from . import *

def GetAbilities() -> Sequence['Ability']:
    def physicalite_brute(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        identite = effect.GetInitiator().GetIdentity()
        this.DealDamage(effect.targets, identite.hand_size, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            physicalite_brute,
        ).SetPlay().SetLabel()
        .SetTarget(Enemy),
    ]
