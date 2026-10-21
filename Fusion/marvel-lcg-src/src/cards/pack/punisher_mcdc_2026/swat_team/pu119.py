from . import *

# SWAT — COMPLOT ANNEXE. Menace de depart 1 (fixe), Boost 1. Setup. Permanent.
# Players cannot thwart this scheme.
# Forced Response : After an enemy is defeated, place 1 threat here (3 threat instead if it had the POLICE trait). Then,
#   if there is 4+ threat here, remove all threat and place 1 wanted counter here.
# If there are 5 or more wanted counters here, the players lose the game.
#
# Cartes de reference : cap/03028 (`UnitCannotThwartTarget(..., cannot_thwart=...)`), sm/bad_publicity/27174a
# (`AfterUnitBeDefeated(Response, ...)`), `Faces.PlaceCountersOn`, `Worlds.SetGameOver(False, effect)` (defaite).
# Setup et Permanent : natifs. Compteur `wanted` ajoute a CardFace.COUNTER.
#
# ⚠ « 3 threat INSTEAD if it had the POLICE trait » : 3 menaces (pas 1+3) ; « 4+ » : des que la menace atteint 4, elle est
# retiree EN ENTIER ; la retrait ne doit PAS « vaincre » SWAT (un complot annexe vide est defait) : on retire les
# jetons sans passer par `RemoveThreatInternal` (qui declenche `Defeated`) ; « 5 or more wanted » : defaite des joueurs.

def GetAbilities() -> Sequence['Ability']:

    def apres_defaite(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        from game.card.face.attribute.can_place_token import CanPlaceToken
        this = effect.this
        defaite = message.trigger
        n = 3 if defaite.HasTrait("POLICE") else 1
        this.PlaceThreatOnSchemes([this], n, effect)
        if this.threat >= 4:
            CanPlaceToken.RemoveTokensInternal(this, this.threat, 'threat', effect, forced=True)
            Faces.PlaceCountersOn([this], 1, 'wanted', effect)
            if this.GetCounters('wanted') >= 5:
                Worlds.SetGameOver(False, effect)

    return [
        *AbilityFactory.UnitCannotThwartTarget(Friend, cannot_thwart="This"),
        AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, Enemy, apres_defaite),
    ]
