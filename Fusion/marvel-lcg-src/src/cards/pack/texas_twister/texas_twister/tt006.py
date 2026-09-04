from . import *

# * Agent T — AMELIORATION, cout 2, [mental]. S.H.I.E.L.D. TITLE.
# Your identity gains the [[S.H.I.E.L.D.]] trait.
# Resource: Exhaust Agent T -> generate a [wild] resource.
#
# CARTES DE REFERENCE
#  - `06009` Mjolnir : `GiveKeywordToAttached(CardFinder(name=...), trait=...)`,
#    l'idiome du trait accorde par une amelioration de heros.
#  - `ab007` (pack albert) : `CanGenerateResources(AbilityType.Resource,
#    Resources("G")).SetCostFunc(CostFunc.Exhaust("This"))`.
#
# TEXTE CONTRE CODE
#  ⚠ LE TRAIT S'ECRIT `S.H.I.E.L.D` SANS POINT FINAL dans le moteur
#    (card_face.py:76). L'ecrire avec, comme la carte l'imprime, sort du
#    `Literal` de typage et ne matcherait aucune carte S.H.I.E.L.D existante.
#  « YOUR IDENTITY gains » -> la carte est attachee a l'identite, donc
#    `GiveKeywordToAttached` sans filtre de nom aurait suffi ; le filtre par
#    nom est conserve pour rester lisible a cote de Mjolnir.
#  « Resource: » -> `AbilityType.Resource` et non `HeroResource` : aucune
#    restriction de forme sur cette carte, contrairement a `ma005`.
#  ⚠ UNE SEULE `CanGenerateResources` PAR CARTE (assert du moteur).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS),
            trait="S.H.I.E.L.D",
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
