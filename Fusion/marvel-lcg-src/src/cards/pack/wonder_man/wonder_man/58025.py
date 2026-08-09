from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.DiscardAll([this], effect)
    def discard_tucked_cost(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        player = effect.GetInitiator()
        if not player:
            return False
        faces = GetTuckedCards(effect, player)
        if (len(faces) < 3):
            return False
        Faces.DiscardAll(faces[:3], effect)
        return True
    return [*AbilityFactory.UnitCannotAttackTarget(CardFinder(name='Wonder Man', card_type=Hero), cannot_attack=True),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, discard_this).SetCostFunc(CostFunc.Exhaust('YourIdentity')),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, discard_this).SetCostFunc(CostFunc.Custom(None, discard_tucked_cost))]
