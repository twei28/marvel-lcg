from . import *

# Psionic Projection. Attachement ILLUSION PSIONIC. « Attach to your identity. Uses (1 illusion counter). As an additional cost for your hero to use a
# basic power, spend a [mental] resource. When Revealed : ... Forced Response : After your hero makes a basic attack or a basic thwart, remove 1
# illusion counter from here. » L'icone du cout est lue contre rm004 (noeuds relies = [mental], `RES=B`).
# Cartes de reference : 13027 (`AdditionalCostToAttack(Hero, CostFunc.Spend(Cost(...)))`), gb011 (attaque ET contre).
# « basic power » d'un HEROS = attaque de base et contre de base (la defense n'est pas un pouvoir).


def GetAbilities() -> Sequence['Ability']:
    def apres_pouvoir(effect: 'Effect', message: 'Message2') -> None:
        RetirerUnCompteurIllusion(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        PoserUnCompteurSiPsionique(),
        AbilityFactory.AdditionalCostToAttack(Hero, CostFunc.Spend(Cost("B")), is_basic_attack=True),
        AbilityFactory.AdditionalCostToThwart(Hero, CostFunc.Spend(Cost("B"))),
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.ForcedResponse, "AttachedHero", apres_pouvoir),
    ]
