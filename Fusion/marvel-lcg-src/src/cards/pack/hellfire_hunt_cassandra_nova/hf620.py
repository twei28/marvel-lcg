from . import *

# Global Opinion Controls (MANIGANCE ANNEXE). Menace de depart 2. « Treat each support's text box as if it were blank. When Revealed : For each
# Cassandra Controls counter in play, place 1 threat here. [star] Boost : Place 2 Cassandra Controls counters on your identity card. »
# Cartes de reference : 39064 / bf023 (`GiveKeywordToInPlayWhenApplyThis(<type>, treat_as_blank=True)`), hf125 (menace posee a la revelation par
# `PlaceThreatOnSchemes([this], n)`), hf124 (boost).
# ⚠ « each support » : TOUS les soutiens en jeu (de tous les joueurs) ; « in play » : toutes les identites ; boost : « YOUR identity » = le joueur
# vise par l'activation.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        n = TotalControlesEnJeu(effect)
        if n > 0:
            this.PlaceThreatOnSchemes([this], n, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        PoserControle(effect, message.GetToPlayer(), 2)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Support, treat_as_blank=True),
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
