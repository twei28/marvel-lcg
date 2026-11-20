from . import *

# * Sinister Flight : EVENEMENT (AERIAL. THWART.), cout 1, [energy]. Classe Hero. (x2)
# Hero Action (thwart): Remove 2 threat from a scheme, ignoring the patrol keyword. Carnage gains the AERIAL trait until the end of the phase.
#
# CARTES DE REFERENCE
#  - Evenement de menee qui ignore Patrouille : `42006` (Natural Flight) : `RemoveThreatFromSchemes(effect.targets, N, effect)` + `.SetPlay().SetLabel('thwart').SetTarget(Scheme2).SetIgnoreKeyword(..)`.
#    ICI seul Patrol est ignore (pas Crisis : le texte ne le dit pas).
#  - Trait gagne jusqu'a la fin de la phase : `GainUntilPhaseEnd(effect, trait=..)` (`face_action.py:513`) ; modele de forme `60017` (`GainUntilRoundEnd(effect, trait=['AERIAL'])`).
#
# TEXTE CONTRE CODE
#  « Hero Action (thwart) » : `HeroAction` + `SetLabel('thwart')` (les cartes qui reagissent a « thwart » le voient). « Remove 2 threat from A scheme » : UN complot, principal ou annexe (`Scheme2`), 2 menaces.
#  « ignoring the PATROL keyword » : `SetIgnoreKeyword('Patrol')` seulement. « CARNAGE gains the AERIAL trait » : l'identite du joueur (face heros, seule face ou l'evenement se joue). « UNTIL THE END OF THE PHASE » : `GainUntilPhaseEnd`, pas le round.
#  Chiffres : cout 1, 2 menaces. Deux exemplaires dans le deck (cas : `ca010`).


def GetAbilities() -> Sequence['Ability']:

    def sinister_flight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        if joueur is not None:
            joueur.GetIdentity().GainUntilPhaseEnd(effect, trait="AERIAL")

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sinister_flight,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2)
        .SetIgnoreKeyword('Patrol'),
    ]
