from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        def action(player: 'Player'):
            for _ in range(8):
                top = player.player_deck.GetTop()
                if not top:
                    break
                Faces.DiscardAll([top], effect)
        Players.ForEachPlayer(effect, action)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
