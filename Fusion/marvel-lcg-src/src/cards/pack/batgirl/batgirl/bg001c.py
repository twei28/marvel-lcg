from . import *

# * Batgirl (Bat Family) — heros. THW 2, ATK 1, DEF 2, main 5, PV 10. « The Oracle » (voir __init__.py : AbiliteOracle).
# Carte de reference : `13001a`... aucune carte officielle ne change une icone de texte : mecanisme MAISON, memorise sur l'effet
# de la carte resolue (WhenCardWouldResolveAbility, modele rz018). « Limit once per round » : LimitOncePerRound.


def GetAbilities() -> Sequence['Ability']:
    return [*AbiliteOracle(), *SuivisDeLaManche()]
