from . import *
def GetAbilities() -> Sequence['Ability']:
    def metro_pd(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        initiator = effect.GetInitiator()
        def deal_damage(targets: Sequence['CardFace']):
            this.DealDamage(targets, 1, effect)
        def remove_threat(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, 1, effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Deal 1 damage to an enemy', deal_damage).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility('Remove 1 threat from a scheme', remove_threat).SetTarget(Scheme2, has_threat=True))
    return [AbilityFactory.FirstPlayerControlThis(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, metro_pd).SetCostFunc(CostFunc.Exhaust('This'))]
