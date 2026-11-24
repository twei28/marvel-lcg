from . import *

# Alien Assault — TRAITRISE. Boost ★ + 1.
# When Revealed: If Predator Warlord is the active villain, stun your identity. If Alien Queen is the active villain, confuse your identity.
# [star] Boost: After this activation ends, do not move the active counter to the next villain.
#
# Cartes de reference : `GiveStatus("Stunned"|"Confused")` ; « do not move the active counter » : garde consommee par le deplacement du
#   compteur (helper `GarderLeCompteur`, lu par 1B / 2B).
#
# ⚠ Mots-pieges : seul le mechant ACTIF compte ; au stade 3/4 il n'y a plus de deplacement (la garde ne sert a rien, elle est oubliee).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        identite = JoueurDuMessage(message, effect).GetIdentity()
        if EstLeMechantActif(effect, WARLORD):
            Faces.GiveStatus([identite], "Stunned", effect)
        elif EstLeMechantActif(effect, REINE):
            Faces.GiveStatus([identite], "Confused", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        GarderLeCompteur(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
