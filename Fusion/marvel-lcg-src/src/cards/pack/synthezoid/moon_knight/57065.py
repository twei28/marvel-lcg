from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        treachery = None
        for face in reversed(list(Worlds.GetEncounterDiscardPile(effect).Get(True))):
            if Treachery.IsType(face):
                treachery = face
                break
        if treachery:
            treachery.Reveal(player, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
