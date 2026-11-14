from . import *

# * Tanalth (II) — MECHANT, stade 2, face B (DISCOVERED). KREE. PV 18[per_hero]. SCH 2. ATK 3.
# Texte identique a gs138b (138B), hors PV et ATK. Voir ce fichier pour les cartes de reference.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesTanalth(2)
