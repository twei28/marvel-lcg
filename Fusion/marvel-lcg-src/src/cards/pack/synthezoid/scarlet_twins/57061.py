from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        identity = player.GetIdentity()
        if not Faces.GiveStatus([identity], 'Confused', effect):
            this.PlaceThreatOnSchemes('MainScheme', 2, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
