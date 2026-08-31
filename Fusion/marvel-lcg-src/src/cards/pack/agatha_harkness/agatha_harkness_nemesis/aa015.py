from . import *

# Burned at the Stake — complot annexe nemesis. Menace 6. Boost 1. Hazard 1.
# Death gains Stalwart.
#
# Cartes de reference (RECETTES-MOTEUR §3) :
#  - le gain de mot-cle en continu : 16140 Sound the Alarms
#    (`GiveKeywordToInPlayWhenApplyThis(Enemy, attack=1)`), transpose en
#    `stalwart=1` sur la SEULE Death du pack — ciblage par `card_ids`
#    (["aa016"]), jamais par nom : « Death » est aussi un vilain officiel
#    (45084a/b, Four Horsemen).
#
# ⚠ C'est LA meche du set : Death est Vulnerable (defaussee si sonnee ou
# desorientee) et « cannot be defeated » — tant que ce complot est en jeu,
# Robuste la rend intouchable par les statuts. Le detruire d'abord.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_ids=["aa016"]),
            stalwart=1,
        ),
    ]
