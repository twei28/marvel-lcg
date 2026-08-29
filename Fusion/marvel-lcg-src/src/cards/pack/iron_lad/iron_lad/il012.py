from . import *

# Ion Amplifiers (2/2) — contenu identique a il011, voir ce fichier pour le
# detail du modele repris.

def GetAbilities() -> Sequence['Ability']:

    def ion_amplifiers_enter(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        Faces.PlaceCountersOn([this], len(CartesTechControlees(player)), 'ion', effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.NonKeyword,
            "This",
            ion_amplifiers_enter,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, "ion")),
    ]
