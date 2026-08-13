from . import *

# In and Out

def GetAbilities() -> Sequence['Ability']:

    def in_and_out(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        PeutRevenirEnMain(this, initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            in_and_out
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
