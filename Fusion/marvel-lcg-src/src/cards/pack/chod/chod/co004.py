from . import *

def GetAbilities() -> Sequence['Ability']:
    def intellect_brut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        identite = effect.GetInitiator().GetIdentity()
        this.RemoveThreatFromSchemes(effect.targets, identite.hand_size, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            intellect_brut,
        ).SetPlay().SetLabel()
        .SetTarget(Scheme2),
    ]
