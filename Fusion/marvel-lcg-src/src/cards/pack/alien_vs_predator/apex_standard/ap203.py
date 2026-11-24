from . import *

# Assault — TRAITRISE (Apex Standard). Boost 1.
# When Revealed (Alter-Ego): This card gains surge.
# When Revealed (Hero): The villain attacks you. Do not move the active villain counter.
#
# Cartes de reference : 01187 Assault (`WhenThisRevealed("Alter-Ego"|"Hero")`, 16116) ; surge gagne : `ThisCardGainSurge` (01187) ; « do not move » :
#   `SansDeplacerLeCompteur`.
#
# ⚠ Mots-pieges : en alter-ego, AUCUNE attaque (et rien a garder) ; le compteur ne bouge pas apres cette attaque (stade 1 comme 2).


def GetAbilities() -> Sequence['Ability']:

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            SansDeplacerLeCompteur(effect, lambda: mechant.DoAttackYou(joueur, effect))

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", ThisCardGainSurge),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
