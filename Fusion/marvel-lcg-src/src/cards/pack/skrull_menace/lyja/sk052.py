from . import *

# Going Ballistic — EVENEMENT AGRESSION, cout 0 [physique]. ATTACK.
# Hero Action (attack): Discard your hand. Deal 2 damage to an enemy (to a maximum of
#   6) for each card discarded this way.
#
# Cartes de reference :
#  - **`27008`** Ticket to the Multiverse : `Faces.DiscardAll(<main>)` ; la liste rendue
#    est celle des cartes REELLEMENT defaussees.
#  - **`16152`** Contingency Plan / **`32045`** Team Strike : un evenement « (attack) »
#    = `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('attack')` + `SetTarget(Enemy)`,
#    degats par `this.DealDamage` (les degats d'un evenement sont ceux de l'identite,
#    event.py:61 ; le label `attack` les livre a Sonne/Desoriente).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Discard YOUR hand » : toute la main, sans choix (l'evenement jouee n'en fait plus
#    partie : il est en zone de traitement).
#  - « 2 damage FOR EACH card discarded » : 2 x N ; « TO A MAXIMUM OF 6 » : plafond sur
#    les DEGATS (6), pas sur les cartes : on defausse toute la main, on cogne au plus 6.
#  - « (attack) » : label attack ; une cible, « an enemy ».


def GetAbilities() -> Sequence['Ability']:

    def going_ballistic(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        defaussees = Faces.DiscardAll(list(joueur.hand_cards.Get(True)), effect)
        degats = min(6, 2 * len(defaussees))
        if degats > 0 and effect.targets:
            this.DealDamage(effect.targets, degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            going_ballistic,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
