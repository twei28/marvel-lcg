from . import *
def GetAbilities() -> Sequence['Ability']:
    def stand_with_me(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        lc = Worlds.FindCardOnField(effect, name='Luke Cage')
        if not lc:
            return
        Faces.GiveStatus([lc], "Tough", effect)
        n = min(lc.tough, 5)
        this.RemoveThreatFromSchemes(effect.targets, n, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, stand_with_me).SetPlay().SetLabel('thwart').SetTarget(Scheme2, range=(1, 1))]
