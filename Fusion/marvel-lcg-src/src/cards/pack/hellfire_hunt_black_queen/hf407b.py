from . import *

# Beneath the Sun (le JOUR, face B de l'environnement recto-verso). « enters play with 3[per_hero] time counters. If there are no time counters
# here, flip this card. Each identity gets +1 to each of its basic powers. Forced Response : After a character uses a basic power or an enemy
# activates, remove 1 time counter here. » Cartes de reference : 06007 Asgard (`GiveKeywordToInPlayWhenApplyThis(Identity, ...)`), hf407a.


def GetAbilities() -> Sequence['Ability']:
    return AbilitesDuTemps(nuit=False)
