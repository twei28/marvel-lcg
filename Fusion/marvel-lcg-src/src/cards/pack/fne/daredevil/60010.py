from . import *
def GetAbilities() -> Sequence['Ability']:
    def living_lie_detector(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        for target in effect.targets:
            amount = 2 + len(target.GetAttachedUpgrades())
            this.RemoveThreatFromSchemes([target], amount, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, living_lie_detector).SetPlay().SetLabel('thwart').SetTarget(Scheme2, has_threat=True)]
