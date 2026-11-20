from . import *

# Mental Awareness (x2) : AMELIORATION (SKILL. PSIONIC.), cout 1, [wild]. Classe Hero.
# Resource: Exhaust Mental Awareness -> generate a [wild] resource for a [[PSIONIC]] card.
#
# CARTES DE REFERENCE
#  - `08007` Black Widow's Gauntlet / `46004` Power Belt : `CanGenerateResources(Resource, Resources("G"), for_card=CardFinder2("TRAIT")).SetCostFunc(CostFunc.Exhaust("This"))`.
#
# TEXTE CONTRE CODE
#  « Resource » (PAS « Hero Resource ») : `AbilityType.Resource`, utilisable aussi en alter-ego. « a PSIONIC card » : la ressource ne paie qu'une carte portant le trait PSIONIC. La ressource [wild] imprimee du coin
#    (`desc.RES = G`) est celle de la carte defaussee en ressource, autre chose.
#  Chiffres : cout 1, 1 ressource [wild].


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            for_card=CardFinder2("PSIONIC"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
