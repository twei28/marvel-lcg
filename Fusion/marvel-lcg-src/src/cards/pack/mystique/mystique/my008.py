from . import *

# Shapeshifter Focus (Focus Metamorphe) : AMELIORATION (SKILL.), cout 1, [mental].
# Hero Resource: Exhaust Shapeshifter Focus -> generate a [wild] resource for a SHAPESHIFTER card.
#
# CARTES DE REFERENCE
#  - `ra012` : `CanGenerateResources(AbilityType.HeroResource, resources_fn=..).SetCostFunc(CostFunc.Exhaust("This"))` pour une ressource de HEROS payee par inclinaison de la carte.
#  - `bs005` : `CanGenerateResources(.., Resources(..), CardFinder2("TECH"))` pour « for a <TRAIT> card » ; ici `SHAPESHIFTER` (trait des evenements du deck).
#
# TEXTE CONTRE CODE
#  « HERO resource » : seulement en forme heros. « generate a [WILD] resource » : `Resources("G")` (une ressource, joker). « for a SHAPESHIFTER card » : uniquement pour jouer/payer une carte portant le trait SHAPESHIFTER.
#    « Exhaust » : cout, la carte doit etre redressee.
#  Chiffres : cout 1, une ressource.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            CardFinder2("SHAPESHIFTER"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
