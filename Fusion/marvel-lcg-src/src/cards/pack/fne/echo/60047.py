from . import *
def GetAbilities() -> Sequence['Ability']:
    def muscle_memory(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        placed = initiator.GetIdentity().GetPlacedCardArea().Get()
        if not placed:
            return
        def action(targets: Sequence['CardFace']):
            Faces.AddToHand(list(targets), initiator, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Add a tucked event to your hand', action).SetTarget(list(placed), range=(1, 1)))
    def check_has_tucked(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        return (len(initiator.GetIdentity().GetPlacedCardArea().Get()) > 0)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, muscle_memory, conditions=[check_has_tucked]).SetCostFunc(CostFunc.Exhaust('This'))]
