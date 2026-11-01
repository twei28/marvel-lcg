from . import *

# Sebastian Shaw (stade II), vilain. « Absorb » + Forced Interrupt a l'attaque : voir `AbilitesDeShaw` (__init__.py).
# Cartes de reference : the_hunger_core / shadowland Elektra (`WhenUnitWouldAttack(ForcedInterrupt, "This")` + `GainATKForThisAttack`), sk151
# (`AfterUnitTookDamage` « After X takes damage », `message.took_damage`).


def GetAbilities() -> Sequence['Ability']:
    return AbilitesDeShaw()
