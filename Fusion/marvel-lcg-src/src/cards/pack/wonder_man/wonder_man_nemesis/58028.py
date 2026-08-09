from . import *
def GetAbilities() -> Sequence['Ability']:
    def scythe_strike(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        reaper = Worlds.FindCardOnField(effect, name='Grim Reaper', card_type=Minion)
        if reaper:
            reaper.DoActivate(player, effect)
            return
        player.GetIdentity().TakeIndirectDamage(this, 2, effect)
    return [AbilityFactory.WhenThisRevealed(None, scythe_strike)]
