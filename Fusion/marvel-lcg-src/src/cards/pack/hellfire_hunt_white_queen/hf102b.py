from . import *

# White Queen, forme B (DIAMOND), stade 102. « [star] Forced Response : After White Queen schemes, flip this card. » ;
# « Forced Interrupt : When White Queen would take any amount of damage from an attack, discard the top card of the encounter deck.
# Reduce damage from that attack by the number of boost icons discarded this way. »
# Steady et Retaliate 1 : mots-cles lus par le moteur dans `desc` (stade II seulement).
# Cartes de reference : 21173 Master of Illusions (`WhenUnitWouldTakeDamage` ForcedInterrupt `is_from_attack`, `PreventDamage`),
# 01159 Ritual Combat (`FacesCounter.CountTotalBoostIcons` des cartes defaussees), tk001a Bebop (retournement).


def GetAbilities() -> Sequence['Ability']:
    return [ReponseForceeFormeB(), InterruptionForceeFormeB()]
