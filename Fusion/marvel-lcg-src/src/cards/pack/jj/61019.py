from . import *
def GetAbilities() -> Sequence['Ability']:
    def search_side_scheme(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        player = effect.targets[0].GetControlByPlayer()
        faces = Search.SearchForCards(effect, player, include_player_deck=True, card_type=PlayerSideScheme)
        def action(targets: Sequence['CardFace']):
            for face in targets:
                player.GainCard(face, effect)
            player.player_deck.Shuffle(effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Choose a player side scheme', action).SetTarget(faces, range=(0, 1)))
    def remove_threat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, search_side_scheme).SetPlay().SetTarget("Players"),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, remove_threat)
        .SetPlay().SetLabel('thwart').SetTarget(CardFinder(card_type=PlayerSideScheme), range=(1, 1)),
    ]
