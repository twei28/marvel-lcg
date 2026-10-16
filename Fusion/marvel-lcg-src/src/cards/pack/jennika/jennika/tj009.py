from . import *

# * Jennika's Tekko-Kagi — AMELIORATION signature, x1 (14/15, jumelle de tj010).
# NINJA. TEKKO-KAGI. WEAPON. Cout 1, [energy].
# Each [[TEKKO-KAGI]] upgrade you control gains: "Hero Resource: Exhaust this card ->
#   generate a [wild] resource for a Shinobi card."
#
# Cartes de reference :
#  - `leonardo/tl011` Leonardo's Katana : MEME montage — octroi d'une ressource
#    wild restreinte a toutes les armes du trait, par le couple Can/Do
#    `GenerateResources` donne via `GiveKeywordToInPlayWhenApplyThis(...,
#    given_abilities=[...])` (decision utilisateur du 15/10/2026 pour les armes
#    jumelles) ;
#  - `trors/spider_woman/04033` Finesse : « generate a [wild] resource for an
#    aspect card » = `CanGenerateResources(HeroResource, Resources("G"),
#    CardFinder(card_class=...))`.
#
# ⚠ Mots-pieges :
#  - « EACH TEKKO-KAGI upgrade you control GAINS » : l'aptitude est donnee a CHAQUE
#    Tekko-Kagi controle, y compris CETTE carte et tj010 (qui n'a pas de ressource
#    propre : sans tj009 en jeu, tj010 ne produit aucune ressource) ;
#  - « Hero RESOURCE » : forme heros uniquement ;
#  - « generate a [wild] resource FOR A SHINOBI CARD » : la ressource wild ne paie
#    QUE les cartes portant une classe Shinobi (Bushido, Ninjutsu, Kuji-Kiri,
#    Taijutsu) ;
#  - UNE SEULE `CanGenerateResources` par carte (assert card_player.py).


def GetAbilities() -> Sequence['Ability']:

    ressource_donnee = AbilityFactory.CanGenerateResources(
        AbilityType.HeroResource,
        Resources("G"),
        CarteShinobi(),
    ).SetCostFunc(CostFunc.Exhaust("This"))
    depense_donnee = AbilityFactory.DoGenerateResources(
        AbilityType.HeroResource,
        "This",
    )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="TEKKO-KAGI", card_type=Upgrade),
            control_by="You",
            given_abilities=[ressource_donnee, depense_donnee],
        ),
    ]
