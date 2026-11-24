from . import *

# "Hush Now Baby"
# SONG.
# Hero Action: Stun and confuse an enemy.
# Showtime!: Each player draws 1 card.
#
# UNE seule cible recoit les DEUX statuts : « stun and confuse an enemy ».
#
# Cible : `canbe_status=["Stunned", "Confused"]`, l'un OU l'autre, comme la
# carte officielle de meme texte 04036 Pheromones. Jusqu'au 20/10/2026 le
# filtre etait `canbe_stunned=True` : un ennemi deja etourdi (mais pas
# desoriente) n'etait plus une cible legale, alors que la carte peut encore le
# desorienter (backlog 12, cas « un ennemi DEJA etourdi »).


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
        .SetTarget(Enemy, canbe_status=["Stunned", "Confused"]),
        Showtime(showtime),
    ]
