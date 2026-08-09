from . import *
def GetAbilities() -> Sequence['Ability']:
    def contingency_planning(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        for face in effect.targets:
            this.TuckCardUnderHere(face, effect)
    def check_no_tucked(effect: 'Effect') -> bool:
        this = effect.this
        return (len(this.GetPlacedCardArea().Get()) == 0)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.AttachedCardCanPlayLikeInHand(CardFinder(card_type=Upgrade)),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, contingency_planning, conditions=[lambda effect, message: check_no_tucked(effect)]).SetTarget(finder=CardFinder(card_type=Upgrade), from_where=['YourHandCards'], range=(1, 1))]
