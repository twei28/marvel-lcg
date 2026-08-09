from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        if player.GetIdentity().HasTrait('HUNTED'):
            this.DoActivate(player, effect)
            return
        for _ in range(2):
            top = player.player_deck.GetTop()
            if top:
                Faces.DiscardAll([top], effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
