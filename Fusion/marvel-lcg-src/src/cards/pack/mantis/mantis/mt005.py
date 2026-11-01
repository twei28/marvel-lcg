from . import *

# Psychic Feat (x3) : EVENEMENT (PSIONIC), cout 0, [energy]. Hero Class.
# Hero Action: Confuse a character you control. Then, confuse an enemy.
#
# CARTES DE REFERENCE
#  - `27110` Robotic Enhancements : `SetTarget("YouControlUnit", canbe_confused=True)` + `Faces.GiveStatus(cibles, "Confused", effect)`.
#  - `27030a` Spider-Man (Miles Morales) / `05015` : `SetTarget2(Enemy, canbe_confused=True)` pour une seconde cible, lue dans `effect.targets2`.
#
# TEXTE CONTRE CODE
#  « a character YOU control » : un personnage du joueur (identite ou allie), pas un ami d'un autre joueur. « Then, confuse an enemy » : seconde cible, ennemi (vilain ou sbire),
#    apres la premiere. Les filtres `canbe_confused` ecartent un Stoique ou un ennemi deja confus. Hero Action : forme heros seulement.
#  Chiffres : cout 0.


def GetAbilities() -> Sequence['Ability']:

    def psychic_feat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        Faces.GiveStatus(effect.targets, "Confused", effect)
        Faces.GiveStatus(effect.targets2, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            psychic_feat,
        ).SetPlay()
        .SetTarget("YouControlUnit", canbe_confused=True)
        .SetTarget2(Enemy, is_optional=False, canbe_confused=True),
    ]
