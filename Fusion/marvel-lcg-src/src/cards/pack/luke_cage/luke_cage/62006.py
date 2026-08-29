from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_discount(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        return True
    def discount_value(effect: 'Effect') -> int:
        lc = Worlds.FindCardOnField(effect, name='Luke Cage')
        return lc.tough if lc else 0
    def sweet_christmas(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        villain = Worlds.FindVillain(effect)
        targets: List['CardFace'] = []
        if villain:
            targets.append(villain)
        player = effect.GetInitiator()
        for minion in Worlds.FindCardsOnField(effect, card_type=Minion):
            if minion.CastTo(Minion).GetEngagedPlayer() == player:
                targets.append(minion)
        this.AttackDamage(targets, 5, effect)
    return [
        AbilityFactory.ReduceCostToPlayThis(discount_value, conditions=[check_discount]),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, sweet_christmas).SetPlay().SetLabel('attack'),
    ]
