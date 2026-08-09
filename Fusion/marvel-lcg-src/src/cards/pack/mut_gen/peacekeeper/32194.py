from . import *
def GetAbilities() -> Sequence['Ability']:
    def mentorship(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 5, effect)
        Faces.ReadyAll(list(initiator.allies.Get()), effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, mentorship).SetLabel('thwart').SetCost(Cost('3')).SetTarget(Scheme2, has_threat=True)]
