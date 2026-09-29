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
    # Errata RRG 1.8 (MC4DB, 29/09/2026) : « (Limit once per phase.) » -- sans
    # cette limite, une traitrise qui revele a son tour Moon Knight bouclait.
    return [AbilityFactory.WhenThisRevealed(None, when_revealed).LimitOncePerPhase()]
