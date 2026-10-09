from . import *

# hs127 Fierce Cheetah
# Ses attaques gagnent piercing.
# Forced Response : apres qu'un personnage du joueur engage attaque Kraven, le Guepard attaque ce joueur.

def GetAbilities() -> Sequence['Ability']:

    def perforer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainPiercing(effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.NonKeyword, "This", perforer),
        ReponseDeMeute(),
    ]
