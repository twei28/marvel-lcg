from . import *
def GetAbilities() -> Sequence['Ability']:
    def active_altruism(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        value = (1 + (2 * EnergyOverpaid(effect, 0, 2)))
        this.RemoveThreatFromSchemes(effect.targets, value, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, active_altruism).SetPlay().SetLabel('thwart').SetTarget(Scheme2, has_threat=True)]
