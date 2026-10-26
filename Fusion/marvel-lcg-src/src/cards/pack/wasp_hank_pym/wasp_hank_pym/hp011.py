from . import *
# Size Manipulation — amelioration, x2. Entre en jeu avec 2 compteurs pym.
# Resource : incline + retire 1 compteur pym -> genere [wild]. Action : incline + retire 1 compteur -> change de forme.
def GetAbilities() -> Sequence['Ability']:
    def entree(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.PlaceCountersOn([this], 2, 'pym', effect)
    def changer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        changer_de_forme(effect)
    return [
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Interrupt,
            "This",
            entree,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'pym')),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            changer,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'pym')),
    ]
