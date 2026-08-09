from . import *
def GetAbilities() -> Sequence['Ability']:
    def deposition(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        PlaySenseUpgradeFree(initiator, effect)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, deposition).SetPlay().SetLabel('thwart').SetTarget(Scheme2, has_threat=True)]
