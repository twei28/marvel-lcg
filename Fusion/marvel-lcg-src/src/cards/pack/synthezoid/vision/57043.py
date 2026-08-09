from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Leader)
        def action(player: 'Player'):
            player.DealEncounterCards(1, effect)
        Players.ForEachPlayer(effect, action)
        this.effect.RegisterTemp(AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, 'This'), unregister_after_exec=False, until_phase_end=True)
    def after_villain_step(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        FlipMassForm(effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, after_villain_step)]
