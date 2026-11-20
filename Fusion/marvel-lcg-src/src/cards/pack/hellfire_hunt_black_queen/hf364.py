from . import *

# Hellfire Conjuration (module Darkhold). Traitrise SPELL, SPELL OF DARKHOLD. « When Revealed : If Darkhold is attached to the villain, take 3
# indirect damages, remove 1 darkspell counter from Darkhold. Otherwise, find Darkhold attachment and reveal it. »
# Cartes de reference : 27080 (`identite.TakeIndirectDamage(this, n, effect)`), `ResolutionDeSort`.


def GetAbilities() -> Sequence['Ability']:
    def sort(effect: 'Effect', joueur: 'Player') -> None:
        joueur.GetIdentity().TakeIndirectDamage(effect.this, 3, effect)

    return [ResolutionDeSort(sort)]
