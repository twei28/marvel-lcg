from . import *
def GetAbilities() -> Sequence['Ability']:
    def camcorder(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        for target in effect.targets:
            alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
            x = max(0, target.health - 2)
            if alias and alias.GetCounters('evidence') >= x:
                alias.RemoveCountersInternal(x, 'evidence', effect)
                Faces.DiscardAll([target], effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, camcorder)
        .SetPlay().SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(CardFinder(card_type=Minion, non_trait="ELITE"), range=(1, 1)),
    ]
