from . import *
def GetAbilities() -> Sequence['Ability']:
    def burstein_process(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        lc = Worlds.FindCardOnField(effect, name='Luke Cage')
        if not lc:
            return
        n = 2 if lc.tough == 0 else 1
        for _ in range(n):
            Faces.GiveStatus([lc], "Tough", effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, burstein_process)
        .SetPlay().SetCostFunc(CostFunc.Exhaust("This")),
    ]
