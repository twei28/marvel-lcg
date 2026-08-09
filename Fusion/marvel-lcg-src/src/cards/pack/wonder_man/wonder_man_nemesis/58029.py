from . import *
def GetAbilities() -> Sequence['Ability']:
    def death_cannot_die(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        reaper = Worlds.FindCardOnField(effect, name='Grim Reaper', card_type=Minion)
        if not reaper:
            reaper = Search.EncounterCard(effect, player, include_discard_pile=True, include_set_aside=True, name='Grim Reaper', card_type=Minion)
            if reaper:
                reaper.Reveal(player, effect)
                return
            return
        reaper.DoActivate(player, effect)
    def death_cannot_die_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        reaper = Worlds.FindCardOnField(effect, name='Grim Reaper', card_type=Minion)
        if reaper:
            RunAt.AfterEnemyActivationEnd(effect, message.would_message, lambda: reaper.DoActivate(player, effect))
    return [AbilityFactory.WhenThisRevealed(None, death_cannot_die),
            AbilityFactory.WhenCardBecomeBoost('This', death_cannot_die_boost)]
