from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        def action(player: 'Player'):
            CardFactory.GenerateCard('21183', player.player_deck, effect.world)
            player.player_deck.Shuffle(effect)
        Players.ForEachPlayer(effect, action)
        this.card.Flip(effect)
        face = this.card.face
        player = Worlds.GetFirstPlayer(effect)
        face.CastTo(Minion).Reveal(player, effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
