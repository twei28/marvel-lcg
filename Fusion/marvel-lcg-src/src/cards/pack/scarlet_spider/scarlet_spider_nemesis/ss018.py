from . import *

# Assassins Guild — SIDE SCHEME
# Each [[ASSASSIN]] enemy gets +1 ATK.
#
# Modele : core/ultron/01136.py (chaque sbire [[Drone]] +1 ATK/+1 PV en
# continu tant qu'Ultron est en jeu), transpose ici a un side scheme :
# `AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("ASSASSIN",
# Enemy), attack=1)`. `Enemy` couvre a la fois les sbires (Bella Donna,
# Harvester, Undead Hand Ninja) et un vilain [[ASSASSIN]] eventuel.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder2("ASSASSIN", Enemy),
            attack=1,
        ),
    ]
