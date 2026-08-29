from . import *

# * Superior Iron Man
#
# Carte de reference : Venom (vnm/venom/20001a.py) "Symbiotic Bond" -- Resource:
# Take 1 damage -> generate a wild resource (Limit once per phase). Meme
# squelette (CanGenerateResources + CostFunc cout-en-degats + LimitOncePerPhase),
# seule la cible du cout change : "YouControlUnit" (un personnage AMI, pas
# seulement soi-meme) au lieu de "YourIdentity".

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.DealDamage(1, "YouControlUnit"))
        .SetName("“What Else?”")
        .LimitOncePerPhase(),
    ]
