from . import *

# The Fist Fits in the Hand — MANIGANCE ANNEXE, 3 menaces par joueur, icone Hazard, 3 icones de boost (tout dans desc). Nemesis 2/5.
# Chaque sbire HAND gagne +1 MAN et +1 ATQ.
#
# CARTE DE REFERENCE : `54029` / `31037` (`*GiveKeywordToInPlayWhenApplyThis(CardFinder2(TRAIT, Minion), ...)`).
# ⚠ « Each HAND minion » : tous les sbires HAND en jeu, quel que soit le joueur engage ; le bonus tombe quand la manigance quitte le jeu.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder2(TRAIT_MAIN, Minion),
            scheme=1,
            attack=1,
        ),
    ]
