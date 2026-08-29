from . import *

# "Hush Now Baby"
# SONG.
# Hero Action: Stun and confuse an enemy.
# Showtime!: Each player draws 1 card.
#
# UNE seule cible recoit les DEUX statuts : « stun and confuse an enemy ».


def GetAbilities() -> Sequence['Ability']:

    def chut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Faces.GiveStatus(effect.targets, "Stunned", effect)
        Faces.GiveStatus(effect.targets, "Confused", effect)

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        # « EACH player », pas seulement toi.
        for joueur in effect.world.players:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chut,
        ).SetPlay().SetLabel()
        .SetTarget(Enemy, canbe_stunned=True),
        Showtime(showtime),
    ]
