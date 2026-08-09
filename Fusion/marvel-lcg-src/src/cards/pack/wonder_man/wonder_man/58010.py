from . import *
def GetAbilities() -> Sequence['Ability']:
    def sunglasses(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        def tuck(targets: Sequence['CardFace']):
            TuckEnergyEventFromDiscard(effect, player, include_resources=True)
        def add_to_hand(targets: Sequence['CardFace']):
            faces = GetTuckedCards(effect, player)
            if not faces:
                return
            def action(chosen: Sequence['CardFace']):
                Faces.AddToHand(list(chosen), player, effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Add a tucked card to your hand', action).SetTarget(faces, range=(1, 1)))
        player.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Tuck an event or resource with a printed [energy] resource under Ionic Physiology', tuck),
            AbilityFactory.ForChoiceAbility('Add a card tucked under Ionic Physiology to your hand', add_to_hand))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterUnitChangeForm(AbilityType.Response, 'You', sunglasses)]
