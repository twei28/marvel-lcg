from . import *
def GetAbilities() -> Sequence['Ability']:
    def starstruck(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        value = initiator.GetHero().attack
        if (value > 0):
            this.DealDamage(effect.targets, value, effect)
        if (EnergyOverpaid(effect, 1, 1) > 0):
            Faces.GiveStatus(list(effect.targets), 'Stunned', effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, starstruck).SetPlay().SetLabel('attack').SetTarget(Enemy)]
