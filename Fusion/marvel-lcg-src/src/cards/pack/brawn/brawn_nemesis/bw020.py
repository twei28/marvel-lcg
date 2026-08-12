from . import *

# * Namor (sbire nemesis) — custom « Rainy »
# Patrol. Toughness.
# [star] Namor gets +X ATK and +X SCH where X equals the number of acceleration
#   tokens in play.
# Forced Interrupt: When Namor schemes, place that threat on Rising Tide
#   instead.
#
# « in play » et pas « here » : les jetons comptent ou qu'ils soient, y compris
# ceux du complot principal. C'est Rising Tide bw019 qui en produit un par
# round, d'ou la boucle : laisser vivre la manigance rend Namor de plus en plus
# dangereux.
#
# Le bonus se relit a chaque mouvement de jeton (`ex_change_on_event`), sans
# quoi il resterait fige a sa valeur d'entree en jeu.

def _jetons_en_jeu(effect: 'Effect') -> int:
    total = 0
    for face in Worlds.FindCardsOnField(effect):
        if CanAccelerationToken.IsType(face):
            total += face.acceleration_token
    return total


def GetAbilities() -> Sequence['Ability']:

    def bonus(effect: 'Effect', ui: List['CardFace']) -> int:
        return _jetons_en_jeu(effect)

    # Modele des Wrecking Crew (Wrecker 07002, Thunderball 07017...) : « place
    # the threat on his side scheme instead of the main scheme ». Le moteur a
    # une fabrique dediee, la redirection ne se bricole pas depuis
    # WhenUnitWouldScheme (dont ChangeSchemeTarget est reste en commentaire).
    def rising_tide(effect: 'Effect') -> 'Scheme2|None':
        return Worlds.FindCardOnField(effect, name="Rising Tide")

    return [
        AbilityFactory.ThisGainKeyword(
            bonus,
            attack=1,
            scheme=1,
            change_on_event=OnEvent.AccelerationToken(None),
        ),

        AbilityFactory.PlaceThreatOnCardWhenThisScheme(
            AbilityType.ForcedInterrupt,
            rising_tide,
        ),
    ]
