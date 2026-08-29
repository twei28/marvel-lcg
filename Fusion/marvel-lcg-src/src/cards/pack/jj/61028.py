from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        for player in Worlds.GetPlayers(effect):
            cards = [f for f in player.discard_pile.Get() if ClassCard.IsType(f) and f.IsClass("IdentitySpecific")]
            def shuffle_back(_targets: Sequence['CardFace'], player: 'Player'=player, cards: Sequence['CardFace']=cards):
                Faces.ShuffleAllTo(cards, player.player_deck, effect)
            def decline(_targets: Sequence['CardFace']):
                pass
            if cards:
                player.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility('Shuffle your identity-specific cards from your discard pile into your deck', shuffle_back),
                    AbilityFactory.ForChoiceAbility('Decline', decline),
                )
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
