from . import *

# * Worldwide Sentinel Deployment (MANIGANCE ANNEXE). Menace de depart 3[per_hero], Victory 1, Hazard 1, Boost 2. « Victory 1. When Revealed : Each player
# search the encounter deck and discard pile for a SENTINEL minion in player order. Put it into play engaged with you. »
# Cartes de reference : hf381 (`UneSentinelleParJoueur`), mots-cles/hazard.md (icone Hazard : une carte penchee a croix, rien dessous : lue sur le scan).


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.WhenThisRevealed(None, UneSentinelleParJoueur)]
