from . import *
def GetAbilities() -> Sequence['Ability']:
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    def check_hela(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        hela = Worlds.FindCardOnField(effect, name='Hela')
        if hela and hela.HasTrait('WOUNDED'):
            return False
        return True
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        def action(player: 'Player'):
            card = CardFactory.GenerateCard('21187a', player.additional_discard_pile, effect.world)
            card.face.PutIntoPlay(player, effect, under_control=True)
        Players.ForEachPlayer(effect, action)
        this.card.Flip(effect)
        face = this.card.face
        face.CastTo(EncounterSideScheme).Reveal(Worlds.GetFirstPlayer(effect), effect)
    return [AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove, conditions=[check_hela]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
