from . import *

# Nova Flame — custom « DesignHacker »
# Hero Action (attack): Exhaust Human Torch -> place up to 3 flame counters
# on an enemy, then deal 7 damage to that enemy. This attack gains overkill.
#
# LENIENT : « up to 3 » est joué comme 3 (le plafond de Flame On! s'applique
# de toute façon) ; le choix d'en placer moins n'est pas proposé.

def GetAbilities() -> Sequence['Ability']:

    def nova_flame(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        Faces.PlaceCountersOn(effect.targets, 3, 'flame', effect)

        cibles = [x for x in effect.targets if x.IsInPlay()]
        if cibles:
            this.DealDamage(cibles, 7, effect, property=AttackProperty(overkill=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            nova_flame
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetTarget(Enemy),
    ]
