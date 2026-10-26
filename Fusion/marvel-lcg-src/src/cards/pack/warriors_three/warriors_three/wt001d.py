from . import *


def GetAbilities() -> Sequence['Ability']:
    # « Hero Resource: Exhaust <heros> → generate a resource » : l'identite (heros ACTIF) s'incline. Le changement de heros
    # est une capacite de la carte-titre (wt002) et de Leap into Action (wt015) ; « To change to alter-ego, flip The
    # Warriors Three » est le « Change To » du moteur (CORRECTIF player_setup.py : pas de changement libre heros -> heros).
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("R"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
