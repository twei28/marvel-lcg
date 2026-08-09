from . import *
def GetAbilities() -> Sequence['Ability']:
    def rascal_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        Unused(this)
        boost_card = message.trigger
        if not Treachery.IsType(boost_card):
            return
        player = message.GetToPlayer()
        def deal(targets: Sequence['CardFace']):
            Faces.FlipAllTo([boost_card], False, effect)
            Faces.MoveAllTo([boost_card], player.dealt_encounter_cards, effect)
        player.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Deal this treachery to yourself as a facedown encounter card', deal),
            AbilityFactory.ForChoiceAbilityWithCost(Cost('1')))
    return [AbilityFactory.WhenCardBecomeBoost(None, rascal_boost, activating_enemy='This'),
            AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, 'This', AvatarWouldBeDefeated)]
