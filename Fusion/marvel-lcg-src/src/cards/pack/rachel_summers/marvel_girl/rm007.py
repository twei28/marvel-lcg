from . import *

# Temporal Reversal (x2) — EVENEMENT, cout 0 (mental), SUPERPOWER. TEMPORAL. « Max 1 per round. »
# Action: Take an additional turn after this one. At the end of this turn, perform each of the following in order:
#  - Discard any number of cards, and discard down to your hand size.
#  - Draw up to your hand size.
#  - Ready all of your cards.
#
# CARTES DE REFERENCE : `27032` Double Life (`.MaxOnePerRound()` sur un evenement). AUCUNE carte du jeu ne donne un tour de
# plus : MOTEUR (`CORRECTIF`) — la carte pose le drapeau `RM_TOUR_SUPPLEMENTAIRE`, `World.PlayerPhase` joue le tour en plus
# apres celui-ci, et `PlayerPhase.FinDeTourSupplementaire` fait les trois etapes (les deux premieres sont celles de la fin de
# phase : `MayDiscardHandCardsAndDrawUpToMax`).
#
# MOTS-PIEGES : « after THIS one » = juste apres le tour en cours, avant le joueur suivant ; « Max 1 per round » (un seul tour
# de plus par round et par joueur) ; les etapes se jouent a la FIN du tour qui a joue la carte, pas du tour supplementaire.
def GetAbilities() -> Sequence['Ability']:
    def temporal_reversal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        effect.GetInitiator().flag.Update("RM_TOUR_SUPPLEMENTAIRE", 1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            temporal_reversal,
        ).SetPlay().SetLabel()
        .MaxOnePerRound(),
    ]
