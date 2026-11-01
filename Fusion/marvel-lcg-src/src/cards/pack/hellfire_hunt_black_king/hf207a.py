from . import *

# Black King (face A), attachement TITLE Permanent. Mis en jeu par le Setup de 1A (hf204a), il s'attache a Sebastian Shaw.
# « King's Tactic » : voir `TactiqueDuRoi` (__init__.py).
# Cartes de reference : tk007a (Hog Wild, attachement a deux faces : `AttachToFaceWhenPutIntoPlay(SurLeVilain(...))`, `card.Flip`),
# sk151 (`AfterUnitTookDamage(..., "AttachedEnemy", ...)`). Permanent : desc, natif (has_permanent.py).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(SurShaw()),
        TactiqueDuRoi(False),
    ]
