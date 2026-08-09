from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        faces = ([f for f in player.allies.Get()] + [f for f in player.supports.Get()])
        if not faces:
            this.GainSurge(1, effect)
            return
        best = max(faces, key=lambda f: int(str(f.paper.desc.get('Cost', '0')).rstrip('*') or 0))
        cost = int(str(best.paper.desc.get('Cost', '0')).rstrip('*') or 0)
        Faces.DiscardAll([best], effect)
        if (cost > 0):
            this.PlaceThreatOnSchemes('MainScheme', cost, effect)
        else:
            this.GainSurge(1, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
