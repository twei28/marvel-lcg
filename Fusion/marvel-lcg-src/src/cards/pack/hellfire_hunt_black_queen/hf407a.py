from . import *

# Under the Moonlight (la NUIT, face A de l'environnement recto-verso). « enters play with 3[per_hero] time counters. If there are no time
# counters here, flip this card. Forced Interrupt : When Black Queen would activate, give her 1 more boost card. Forced Response : After a
# character uses a basic power or an enemy activates, remove 1 time counter here. » Les trois blocs communs aux deux faces vivent dans
# `AbilitesDuTemps` (__init__.py). Cartes de reference : gs183 (`WhenEnemyActivateAgainstYou` + `GiveAdditionalBoostCardForThisActivation`),
# 50090a Alert Level / 39026a (`card.Flip`), `IfThereIsNoCounterHere`.


def GetAbilities() -> Sequence['Ability']:
    return AbilitesDuTemps(nuit=True)
