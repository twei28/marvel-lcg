from . import *
def GetAbilities() -> Sequence['Ability']:
    def see_no_evil_hear_no_evil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        def deal_damage(targets: Sequence['CardFace']):
            this.DealDamage(targets, 3, effect)
        def remove_threat(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, 3, effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Deal 3 damage to an enemy', deal_damage).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility('Remove 3 threat from a scheme', remove_threat).SetTarget(Scheme2, has_threat=True),
            repeat=2)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, see_no_evil_hear_no_evil).SetPlay().SetLabel('attack', 'thwart').SetTarget('TeamUp')]
