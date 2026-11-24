from . import *

# Xandar — PLAYER ENVIRONMENT. PLANET. Planet deck (4/5).
#
# Texte imprime :
#  « Arrive: The arriving character gains +2 DEF until the end of the
#    round. »
#  « Depart: Ready the departing character. »
#
# CARTES DE REFERENCE : voir pc005 Sakaar (meme gabarit). `Faces.ReadyAll`
# pour « ready the departing character ».


def GetAbilities() -> Sequence['Ability']:

    def ici(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet|Message.AfterCharacterDepartPlanet') -> bool:
        return effect.this == message.planet_face

    def arrivee(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet') -> None:
        message.character_face.GainUntilRoundEnd(effect, defense=2)

    def depart(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> None:
        Faces.ReadyAll([message.character_face], effect)

    return [
        Ability(AbilityType.Response, Message.AfterCharacterArrivePlanet, [ici], arrivee),
        Ability(AbilityType.Response, Message.AfterCharacterDepartPlanet, [ici], depart),
    ]
