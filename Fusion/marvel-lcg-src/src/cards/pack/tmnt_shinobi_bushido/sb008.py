from . import *

# Self-Control — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 2, [mental].
# Uses (3 samurai counters).
# Resource: Exhaust this card and remove 1 samurai counter from it -> generate a [wild] resource.
# « The path to self-control is long. » —Michelangelo
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md, NATIF) ; samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference :
#  - « Resource: Exhaust this card -> generate a [wild] resource » : `trors/hawkeye/04010` Expert Marksman
#    (`CanGenerateResources(AbilityType.Resource, Resources("G"))` + `CostFunc.Exhaust("This")`), SANS restriction de carte payee
#    (pas d'argument `for_card`) ;
#  - le cout a compteur : `jennika/tj006` (`CostFunc.Counter("This", n, 'samurai')`).
#
# TEXTE CONTRE CODE
#  ⚠ « Resource » (pas Hero Resource) : la ressource est generee dans les DEUX formes de l'identite ; `AbilityType.Resource`.
#  ⚠ L'icone imprimee dans le texte (etoile noire a branches irregulieres) est LE MEME glyphe que celui de `jennika/tj009`
#    Tekko-Kagi (decoupes comparees le 17/10/2026, deja code [wild] et valide) : ressource WILD, `Resources("G")`.
#  ⚠ « Exhaust this card AND remove 1 samurai counter FROM IT » : DEUX couts ; Uses defausse la carte au dernier compteur, ce qui
#    se produit PENDANT un paiement (cas dedie : la carte payee entre quand meme en jeu).
#  ⚠ « generate A resource » : UNE seule ressource par usage ; la ressource paie TOUTE carte (aucune restriction imprimee).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'samurai')),
    ]
