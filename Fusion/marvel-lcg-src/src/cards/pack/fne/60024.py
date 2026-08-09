from . import *

# * De-escalation
# Victory 0.
# When Defeated: Remove an acceleration token from play.
#
# CORRECTIF 4/8/2026 : `Worlds.RemoveAccelerationToken` n'existe pas, la
# capacite plantait a chaque fois que la manigance etait vaincue. On passe par
# les faces qui PORTENT un jeton (`GetAccelerationTokenFaces`) et par le
# retrait de jeton standard.

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        porteurs = [x for x in Worlds.GetAccelerationTokenFaces(effect)
                    if x.acceleration_token > 0]
        if porteurs:
            Faces.RemoveTokensOn(porteurs[:1], 1, 'acceleration_token', effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated),
    ]
