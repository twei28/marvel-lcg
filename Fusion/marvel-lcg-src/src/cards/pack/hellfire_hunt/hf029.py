from . import *

# Shattered Confidence (POTENTIAL ALLY, Armor). Victory 1. When Defeated: le joueur qui la defait cherche Armor dans la zone mise de cote.
# Carte de reference : 04141 Prison Camps (`WhenSchemeBeDefeated(..., has_defeating_player=True)`), `AbilitePotentialAlly` (__init__.py).
def GetAbilities() -> Sequence['Ability']:
    return [AbilitePotentialAlly("Armor")]
