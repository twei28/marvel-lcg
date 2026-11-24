from . import *

# Sakaar — PLAYER ENVIRONMENT. PLANET. Planet deck (2/5). Pas de cout imprime
# (jamais jouee depuis la main, revelee par Cosmic Surfboard/pc001b).
#
# Texte imprime :
#  « Arrive: The arriving character gains +2 ATK until the end of the
#    round. »
#  « Depart: Deal 2 damage to an enemy. »
#
# CARTES DE REFERENCE
#  - `pc003` Zenn-La : meme gabarit (filtre `effect.this == message.planet_face`
#    sur `AfterCharacterArrivePlanet`/`AfterCharacterDepartPlanet`).
#  - `ls004` Lead The Charge (lady_sif) : `face.GainUntilRoundEnd(effect,
#    attack=1)` pour « gets +N ATK until the end of the round » — PAS un
#    `GainKeyword` manuel (essaye d'abord, inope­rant : `OnResetKeywords`
#    remet le `printed_attack` au prochain recalcul et efface le bonus avant
#    qu'il ne serve, mesure le 05/11/2026 sur ce cas precis).
#  - `01084` Nick Fury (core) : `.SetTarget(Enemy)` + `this.DealDamage(cibles,
#    2, effect)` pour « deal 2 damage to an enemy ».
#
# TEXTE CONTRE CODE
#  « +2 ATK UNTIL THE END OF THE ROUND » : pas permanent — retire au
#    prochain `WhenRoundEnd`, pas a un depart ulterieur.
#  « an enemy » : n'importe lequel, choisi par le joueur (`.SetTarget(Enemy)`).


def GetAbilities() -> Sequence['Ability']:

    def ici(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet|Message.AfterCharacterDepartPlanet') -> bool:
        return effect.this == message.planet_face

    def arrivee(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet') -> None:
        message.character_face.GainUntilRoundEnd(effect, attack=2)

    def depart(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> None:
        Unused(message)
        if not effect.targets:
            return
        effect.this.DealDamage(effect.targets, 2, effect)

    return [
        Ability(AbilityType.Response, Message.AfterCharacterArrivePlanet, [ici], arrivee),
        Ability(AbilityType.Response, Message.AfterCharacterDepartPlanet, [ici], depart).SetTarget(Enemy),
    ]
