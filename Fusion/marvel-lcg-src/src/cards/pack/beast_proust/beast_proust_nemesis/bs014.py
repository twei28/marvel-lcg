from . import *

# Technical Difficulties : COMPLOT ANNEXE, menace de depart 5, boost 2, ACCELERATION 1.
# "Thus conscience does make cowards of us all." — W. Shakespeare & Black Beast
# When Revealed: Place 1 threat on this card for each upgrade in play.
#
# CARTES DE REFERENCE
#  - `27156` Personal Nightmare / `mf015` : `WhenThisRevealed(None, op)` + `this.PlaceThreatOnSchemes([this], n, effect)` pour une manigance annexe qui se charge a la revelation.
#  - `acceleration.md` : `desc.Acceleration` lu NATIVEMENT ; `Worlds.FindCardsOnField(effect, card_type=Upgrade)` pour les ameliorations en jeu.
#
# TEXTE CONTRE CODE
#  « 1 threat for EACH upgrade IN PLAY » : toutes les ameliorations en jeu, de TOUS les joueurs et celles attachees aux ennemis ; une carte glissee sous le Lab n'est PAS en jeu (filtre `IsInPlay`). « on THIS card » : la
#    menace va sur cette manigance, pas sur le complot principal. Acceleration 1 et boost 2 : natifs.
#  Chiffres : menace de depart 5, boost 2, acceleration 1.


def GetAbilities() -> Sequence['Ability']:

    def difficultes_techniques(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)
        n = len([f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade) if f.IsInPlay()])
        if n > 0:
            this.PlaceThreatOnSchemes([this], n, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            difficultes_techniques,
        ),
    ]
