from . import *
def GetAbilities() -> Sequence['Ability']:
    def knuckle_sandwich(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.AttackDamage(effect.targets, 3, effect)
        lc = Worlds.FindCardOnField(effect, name='Luke Cage')
        player = effect.GetInitiator()
        def return_to_hand(_targets: Sequence['CardFace']):
            lc.DiscardTough(effect, rule=1)
            player.GainCard(this, effect)
        def decline(_targets: Sequence['CardFace']):
            pass
        if lc and lc.tough > 0:
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility('Discard a tough status card from Luke Cage to return this event to your hand', return_to_hand),
                AbilityFactory.ForChoiceAbility('Decline', decline),
            )
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, knuckle_sandwich).SetPlay().SetLabel('attack').SetTarget(Enemy, range=(1, 1))]
