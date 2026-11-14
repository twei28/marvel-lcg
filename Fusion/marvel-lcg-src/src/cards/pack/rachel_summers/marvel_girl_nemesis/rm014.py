from . import *

# Hound Program — COMPLOT ANNEXE (nemesis), menace de depart 1, boost 3. « Permanent. »
# Hero Response: After Marvel Girl's turn begins, place 1 threat here. If there is at least 5 threat here, the players lose
# the game.
#
# CARTES DE REFERENCE : `Worlds.SetGameOver(False, effect)` (defaite des joueurs, `27102b`), `this.PlaceThreatOnSchemes([this],
# n, effect)` (poser de la menace SUR la carte), `AfterPlayerTurnBegin` (`22001a`). `Permanent` : cle `desc` (`40105a`).
#
# MOTS-PIEGES : « Hero Response » imprime sur une carte de rencontre : codee en Reponse FORCEE (sinon le joueur ne la
# declencherait jamais : question en attente) ; seulement au tour de MARVEL GIRL en forme heros ; « at least 5 » (>= 5).
def GetAbilities() -> Sequence['Ability']:
    def hound_program(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this
        this.PlaceThreatOnSchemes([this], 1, effect)
        if this.threat >= 5:
            Worlds.SetGameOver(False, effect)

    def tour_de_marvel_girl(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> bool:
        Unused(effect)
        return EstMarvelGirl(message.GetToPlayer())

    return [
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.ForcedResponse,
            "AnyPlayer",
            hound_program,
            conditions=[tour_de_marvel_girl],
        ),
    ]
