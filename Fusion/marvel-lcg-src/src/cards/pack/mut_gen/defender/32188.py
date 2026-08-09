from . import *
def GetAbilities() -> Sequence['Ability']:
    def heroic_intervention(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 5, effect)
        Faces.GiveStatus([initiator.GetIdentity()], 'Tough', effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, heroic_intervention).SetLabel('thwart').SetCost(Cost('3')).SetTarget(Scheme2, has_threat=True)]
