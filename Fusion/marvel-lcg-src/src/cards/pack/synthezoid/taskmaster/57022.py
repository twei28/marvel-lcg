from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        this.DoActivate(player, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
