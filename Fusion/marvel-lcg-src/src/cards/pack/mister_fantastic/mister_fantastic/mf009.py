from . import *

# Stretched Thin — custom « DesignHacker »
# Hero Action (thwart): Remove 2 threat from a scheme. Then, if you have no
# cards remaining in your hand, remove 1 threat from each scheme in play.

def GetAbilities() -> Sequence['Ability']:

    def stretched_thin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

        initiator = effect.GetInitiator()
        if len(list(initiator.hand_cards.Get())) == 0:
            this.RemoveThreatFromSchemes("EachScheme", 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stretched_thin
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
