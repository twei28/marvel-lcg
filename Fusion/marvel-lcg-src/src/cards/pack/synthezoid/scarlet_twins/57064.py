from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer() if hasattr(message, 'GetDefeatingPlayer') else None
        if not player:
            player = Worlds.GetFirstPlayer(effect)
        def action(targets: Sequence['CardFace']):
            Faces.DiscardAll(list(targets), effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard 1 card from your hand', action).SetTarget('YourHandCards', range=(1, 1), canbe_discard=True))
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
