from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        types = set()
        for _ in range(3):
            top = player.player_deck.GetTop()
            if not top:
                break
            types.add(top.paper.type)
            Faces.DiscardAll([top], effect)
        if types:
            player.GetIdentity().TakeIndirectDamage(this, len(types), effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
