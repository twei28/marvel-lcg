from . import *

# Ire of Athena — OBLIGATION. 2 icones de boost.
# Give to the Ares player.
# Increase the cost of each TACTIC you play by 1.
# Alter-Ego Action: Exhaust your alter-ego or discard a TACTIC card from your
#   hand -> discard this card.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau imprime dit « ARES », pas « ... NEMESIS ».
# Son `set_name` est celui du set HEROS, le module vit donc ICI. Piege bt019 /
# nt012 / yd013 / dr010 / bk017 / tt020 / br012 / tg011 / sn011 / bc012 / sf010
# — DOUZIEME fois.
#
# CARTES DE REFERENCE
#  - `sf010` Shame (pack sunfire) / `04165` Martial Law : une obligation qui
#    RESTE en jeu avec un malus continu et une Action pour s'en defaire.
#  - `resources.py:668` `IncreaseResourceCostToPlay(which_card, n, "You")` :
#    la seule fabrique qui AUGMENTE un cout de jeu (sa jumelle
#    `ReduceCostToPlayFaceWhen` le baisse).
#  - RECETTES §5 « Deux couts alternatifs (« A or B ») » : un cout est fige a
#    la construction, le « or » devient DEUX capacites (modeles an003, vv005,
#    br004). Ce ne sont pas des `Play`, la liste blanche de factory.py n'est
#    pas concernee.
#
# TEXTE CONTRE CODE
#  ⚠ « each TACTIC YOU play » -> `CardFinder(trait=TACTIC)` + `"You"` : le
#    controleur de l'obligation, c'est-a-dire le joueur d'Ares. Evenements ET
#    ameliorations TACTIC, y compris ceux joues par God of War (ar007) depuis
#    le deck, puisqu'ils sont JOUES (arbitrage du 07/09).
#  ⚠ « Exhaust your alter-ego OR discard a TACTIC card » -> deux
#    `PlayerActionToDiscardThis(AlterEgoAction)`, l'une avec
#    `CostFunc.Exhaust("YourIdentity")` (en Alter-Ego Action, l'identite EST
#    l'alter-ego), l'autre avec `CostFunc.Discard("YourHandCards", trait=TACTIC,
#    range=(1, 1))`.
#  ⚠ « DISCARD this card » et non « remove from the game » : l'obligation
#    revient dans le deck de rencontre du joueur (lecon sf010, qui dit
#    l'inverse : ne pas recopier la carte modele sans la relire).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.IncreaseResourceCostToPlay(
            CardFinder(trait=TRAIT_TACTIC),
            1,
            "You",
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetName("Exhaust your alter-ego")
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetName("Discard a TACTIC card from your hand")
        .SetCostFunc(CostFunc.Discard("YourHandCards", trait=TRAIT_TACTIC, range=(1, 1))),
    ]
