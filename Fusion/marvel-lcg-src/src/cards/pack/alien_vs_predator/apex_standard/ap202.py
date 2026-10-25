from . import *

# Advance Again — TRAITRISE (Apex Standard). Boost 1.
# When Revealed: The villain schemes. Do not move the active villain counter.
#
# Cartes de reference : 01186 Advance ; « Do not move the active villain counter » : garde consommee par 1B (`SansDeplacerLeCompteur`).
#
# ⚠ Mots-pieges : la menace va sur la manigance du mechant (sa regle ★ s'applique, contrairement a Advance) ; le compteur reste.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            SansDeplacerLeCompteur(effect, lambda: mechant.DoSchemes(joueur, effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
