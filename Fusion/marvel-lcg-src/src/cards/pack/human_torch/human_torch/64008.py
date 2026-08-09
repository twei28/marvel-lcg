from . import *

# Blaze and Daze — custom « DesignHacker »
# Hero Action (attack): Deal 4 damage to an enemy. Then, if they have 3 flame
# counters on them, remove all those counters and stun that enemy.

def GetAbilities() -> Sequence['Ability']:

    def blaze_and_daze(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.DealDamage(effect.targets, 4, effect)

        for target in effect.targets:
            if not target.IsInPlay():
                continue
            if target.GetCounters('flame') >= 3:
                Faces.RemoveCountersOn([target], "All", 'flame', effect)
                Faces.GiveStatus([target], "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            blaze_and_daze
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
