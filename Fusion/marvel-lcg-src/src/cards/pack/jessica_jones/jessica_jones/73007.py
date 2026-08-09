from . import *

# The Truth Hurts — custom « ekAugust »
# Play only if there is a side scheme in play.
# Hero Action (attack): Deal 2 damage to an enemy. If you defeated a side
#   scheme this round, confuse that enemy.

def GetAbilities() -> Sequence['Ability']:

    def the_truth_hurts(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.DealDamage(effect.targets, 2, effect)
        if HasDefeatedSideSchemeThisRound(effect):
            Faces.GiveStatus(effect.targets, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            the_truth_hurts,
            conditions=[IsSideSchemeInPlay],
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
