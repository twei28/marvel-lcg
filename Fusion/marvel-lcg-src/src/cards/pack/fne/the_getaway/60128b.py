from . import *

# The Getaway 1B — 2[per_hero] de depart, cible 9[per_hero], escalade
#   +2[per_hero] : bases desc.
# Forced Interrupt: When the round ends, if there is threat here, do each of
#   the following: 1. Place 1 speed counter here. 2. If Alongside is in play,
#   flip it to Out Front. Otherwise, place 1 additional speed counter here.
# If this stage is completed, the players lose the game.
# ⚠ « if there is threat here » lu AVANT toute action ; Alongside -> Out Front
# passe par RetournerLAttachement (le Flip nu detache, RECETTES §7quater).

def GetAbilities() -> Sequence['Ability']:

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        this = effect.this.CastTo(MainScheme)
        if this.threat <= 0:
            return
        Faces.PlaceCountersOn([this], 1, 'speed', effect)
        alongside = Worlds.FindCardOnField(effect, name="Alongside", card_type=Attachment)
        if alongside is not None:
            RetournerLAttachement(alongside, effect)
        else:
            Faces.PlaceCountersOn([this], 1, 'speed', effect)

    return [
        AbilityFactory.WhenRoundEnd(AbilityType.ForcedInterrupt, None, fin_de_round),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
