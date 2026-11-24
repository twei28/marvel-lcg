from . import *

# Ebon Knight (x4, hf212-hf215). Sbire HELLFIRE, Guard + Patrol + Quickstrike (desc, natif). « [star] Boost : After this activation, deal Ebon Knight
# to you as a facedown encounter card. »
# Cartes de reference : 01121 Weapons Runner (boost qui agit sur LA carte), 49042 (`message.AfterThisActivation`), `player.DealEncounterCard(face, effect)`
# (Puzzle.Deal). ⚠ « deal to YOU » : le joueur qui subit l'activation (`message.GetToPlayer()`).


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.WhenCardBecomeBoost("This", BoostDonnerLeSbire)]
