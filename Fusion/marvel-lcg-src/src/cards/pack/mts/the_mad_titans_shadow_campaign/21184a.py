from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        def action(player: 'Player'):
            face = Search.PlayerCard(effect, player, include_player_deck=True, include_discard_pile=True, may=True)
            if face:
                Faces.AddToHand([face], player, effect)
        Players.ForEachPlayer(effect, action)
        this.card.Flip(effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
