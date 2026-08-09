from . import *
def GetAbilities() -> Sequence['Ability']:
    def surprise(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        def remove_threat(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, 3, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove 3 threat from among schemes', remove_threat).SetTarget(Scheme2, has_threat=True))
        def confuse(targets: Sequence['CardFace']):
            Faces.GiveStatus(list(targets), 'Confused', effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Confuse an enemy', confuse).SetTarget(Enemy))
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterUnitThwartScheme(AbilityType.HeroResponse, 'YourHero', None, surprise)]
