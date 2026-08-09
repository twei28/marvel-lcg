from . import *

# Hit the Streets — custom « ekAugust »
# Hero Action (thwart): Remove 3 threat from a scheme. Remove 1 additional
#   threat from that scheme for each side scheme in play.

def GetAbilities() -> Sequence['Ability']:

    def hit_the_streets(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        value = 3 + len(Worlds.GetSideSchemes(effect))
        this.RemoveThreatFromSchemes(effect.targets, value, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hit_the_streets,
        ).SetPlay()
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
