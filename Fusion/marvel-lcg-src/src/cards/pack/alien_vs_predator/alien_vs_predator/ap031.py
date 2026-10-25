from . import *

# Lethal Ambush — TRAITRISE. Boost 2.
# When Revealed: Discard the top 7 cards of the encounter deck. Put the first minion discarded this way into play engaged with you. Then, the
#   villain and each minion engaged with you attacks you.
#
# Cartes de reference : `Worlds.DiscardEncounterCards(7)` ; mise en jeu engagee : 07001a / pd008 ; « the villain ... attacks you » :
#   `DoAttackYou` (16116), chaque sbire engage aussi.
#
# ⚠ Mots-pieges :
#  - « the FIRST minion discarded » : le premier dans l'ordre de defausse (un seul) ;
#  - « the villain » = le mechant actif (regle du scenario) ; « EACH minion engaged with you » : y compris le nouveau.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        defaussees = Worlds.DiscardEncounterCards(7, effect)
        premier = next((f for f in defaussees if Minion.IsType(f)), None)
        if premier is not None and premier.PutIntoPlay(joueur, effect):
            premier.CastTo(Minion).EngagePlayer(joueur, effect)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None and not effect.world.is_game_over:
            mechant.DoAttackYou(joueur, effect)
        for sbire in list(joueur.GetEngagedMinions()):
            if effect.world.is_game_over:
                return
            if sbire.IsInPlay():
                sbire.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
