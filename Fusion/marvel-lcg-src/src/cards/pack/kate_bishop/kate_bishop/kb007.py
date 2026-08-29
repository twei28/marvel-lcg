from . import *

# Anchor Points — PERSONA
# Resource: Exhaust Anchor Points -> generate a [wild] resource for a SKILL
#   card.
#
# Modele : Magneto's Helmet (magneto/magneto/49003.py), meme structure
# `AbilityFactory.CanGenerateResources(AbilityType.Resource, Resources("G"),
# for_card=...)`. "SKILL" est un trait de carte (`CardFinder2("SKILL")`), pas
# une carte nommee.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            for_card=CardFinder2("SKILL"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
