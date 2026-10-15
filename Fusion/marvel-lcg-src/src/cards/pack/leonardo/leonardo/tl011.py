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
# TODO-QUESTION Q2 — « Each KATANA upgrade you control GAINS ... » est un
# OCTROI d'aptitude. Aucune carte joueur du depot n'octroie une aptitude de
# ce genre (`GiveAbilityToInPlayWhenApplyThis` n'est utilise que pour des
# cartes Rencontre). Rendu retenu : CHAQUE katana porte sa propre
# CanGenerateResources — tl011 ici, tl012 sous la condition « un exemplaire de
# tl011 est en jeu sous votre controle » (voir tl012). Equivalent en jeu pour
# les deux katanas du pack ; ne couvre PAS un futur KATANA d'un autre pack.
#
# Mots-pieges :
#  - « Hero RESOURCE » : forme de heros uniquement (type HeroResource) ;
#  - « for an IDENTITY-SPECIFIC card » : toute carte de classe `Hero` (le
#    kit), pas un evenement seulement ;
#  - « generate a [wild] » : `Resources("G")` ;
#  - l'insert dit « either KATANA (or both) » : deux katanas, deux sources.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            CardFinder(card_class="IdentitySpecific"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
