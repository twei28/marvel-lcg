from . import *

# Dead End — COMPLOT ANNEXE. Menace de depart 2 par joueur, Boost 3, Crisis 1. Assault.
# When Revealed : If Shifting Corridors is in play, remove 1 passage counter from it ; otherwise, place 1[per_hero] threat here.
#
# Cartes de reference : shadowland/shadows_in_the_night/sl009 (`PlaceThreatOnSchemes([this], "1*", effect)`), web_of_deceit/the_lizard/__init__ (`Faces.RemoveCountersOn`),
# assault.md (Assault et Crisis natifs).
# ⚠ Mots-pieges : « from IT » : le compteur est retire de Shifting Corridors (pas de cette manigance) ; si c'est le DERNIER passage, les joueurs perdent (sl037) ;
#  « 1[per_hero] » : 1 par joueur ; « otherwise » : Shifting Corridors n'est plus en jeu (stade 2).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        corridors = Corridors(effect)
        if corridors is not None:
            Faces.RemoveCountersOn([corridors], 1, 'passage', effect)
        else:
            this.PlaceThreatOnSchemes([this], "1*", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
