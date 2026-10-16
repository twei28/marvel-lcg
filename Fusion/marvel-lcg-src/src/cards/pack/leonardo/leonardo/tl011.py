from . import *

# * Leonardo's Katana — AMELIORATION signature, x1. KATANA. NINJA. WEAPON.
# Cout 1, [physical]. Restricted.
# Each [[KATANA]] upgrade you control gains: "Hero Resource: Exhaust this card
#   -> generate a [wild] resource for an identity-specific card."
#
# Cartes de reference :
#  - `rogue/38019` X-Gene : `CanGenerateResources(AbilityType.Resource,
#    Resources("G"), CardFinder(card_class="IdentitySpecific", ...))` +
#    `CostFunc.Exhaust("This")` — ressource wild RESTREINTE aux cartes
#    specifiques a l'identite ;
#  - `ho009` Goblin Helmet pour le type `HeroResource` ;
#  - `ls010` Sif's Spear pour `CanPlayThisUpgradeCard()` + `Restricted`.
#
# ⚠ `Restricted` est une BASE AUTOMATIQUE (`desc.Restricted`) : aucun module.
# ⚠ UNE SEULE `CanGenerateResources` PAR CARTE (assert card_player.py:82-84).
#
# DECISION UTILISATEUR (15/10/2026, decisions-phase-b.md) : VRAI OCTROI
# d'aptitude. « Each KATANA upgrade you control GAINS ... » :
# `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(trait="KATANA",
# card_type=Upgrade), control_by="You", given_abilities=[...])` (modele :
# michelangelo/tm011, Nunchuck). L'aptitude donnee est enregistree PAR
# PORTEUR (`RegisterGiven`, face_effect.py:69) et retiree quand tl011 quitte
# le jeu : tl012 n'a donc AUCUNE ressource propre (son script n'en porte plus).
# La ressource est le couple « Can/DoGenerateResources » : la premiere
# annonce la ressource au paiement, la seconde la depense ; hors `GetAbilities`
# statique le moteur ne fabrique pas la seconde tout seul, on la donne aussi.
#
# Mots-pieges :
#  - « Hero RESOURCE » : forme de heros uniquement (type HeroResource) ;
#  - « for an IDENTITY-SPECIFIC card » : toute carte de classe `Hero` (le
#    kit), pas un evenement seulement ;
#  - « generate a [wild] » : `Resources("G")` ;
#  - l'insert dit « either KATANA (or both) » : deux katanas, deux sources.


def GetAbilities() -> Sequence['Ability']:

    ressource_donnee = AbilityFactory.CanGenerateResources(
        AbilityType.HeroResource,
        Resources("G"),
        CardFinder(card_class="IdentitySpecific"),
    ).SetCostFunc(CostFunc.Exhaust("This"))
    depense_donnee = AbilityFactory.DoGenerateResources(
        AbilityType.HeroResource,
        "This",
    )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="KATANA", card_type=Upgrade),
            control_by="You",
            given_abilities=[ressource_donnee, depense_donnee],
        ),
    ]
