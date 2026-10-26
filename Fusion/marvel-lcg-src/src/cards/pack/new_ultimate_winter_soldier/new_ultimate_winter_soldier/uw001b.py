from . import *

# * Logan (face ALTER EGO) — EARTH-6160. MUTANT. SOLDIER. PV 10, REC 6, main 6.
# Shuck! — Setup: Search your deck and discard pile for the Wolverine's Claws upgrade and put it into play.
#
# Carte de reference : `35001b` * Logan (Wolverine officiel) : la meme phrase est rendue par
# `AbilityFactory.SetupPutIntoPlay(["35002"])` ET par `set_aside: ["35002"]` dans le deck de depart. Ici
# `uw002`, mise de cote par `deck/starter/new_ultimate_winter_soldier.json` (les Griffes ne sont donc ni dans le deck
# ni dans la main de depart : le texte « search your deck and discard pile » trouve toujours la carte).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.SetupPutIntoPlay(
            [GRIFFES_ID],
        ),
    ]
