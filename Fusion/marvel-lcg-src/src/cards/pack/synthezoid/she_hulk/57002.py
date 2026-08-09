from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Leader)
        def action(player: 'Player'):
            player.DealEncounterCards(1, effect)
        Players.ForEachPlayer(effect, action)
        this.effect.RegisterTemp(AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, 'This'), unregister_after_exec=False, until_phase_end=True)
    def alter_ego_flips(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Leader)
        identity = message.trigger
        this.DealDamage([identity], 1, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            AbilityFactory.AfterUnitChangeForm(AbilityType.ForcedResponse, None, alter_ego_flips, to_form=Hero)]
