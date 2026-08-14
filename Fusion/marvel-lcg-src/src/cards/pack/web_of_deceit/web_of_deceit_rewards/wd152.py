from . import *

# Web-Shooter (arbre Web-Spinner)
#
# Le nom et le texte sont ceux de la carte officielle 01008, au mot pres. Le
# module aussi : c'est la meme carte, rendue au meme prix.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G")
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, "web")),
    ]
