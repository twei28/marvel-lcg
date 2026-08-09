from . import *
from cards.pack.mut_gen.campaign import ShuffleTopFuturePastIntoEncounter
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        def action(player: 'Player'):
            face = Search.PlayerCard(effect, player, include_player_deck=True, card_type=Ally, may=True)
            if face:
                this.TuckCardUnderHere(face, effect)
        Players.ForEachPlayer(effect, action)
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        ShuffleTopFuturePastIntoEncounter(effect)
        this = effect.this.CastTo(EncounterSideScheme)
        this.card.Flip(effect)
        face = this.card.face
        face.CastTo(Environment).Reveal(Worlds.GetFirstPlayer(effect), effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
