from . import *

# Crimson Scythe — EVENEMENT (ATTACK. THWART), cout 2, [energy].
# Play only if you control the Slayer Scythe.
# Hero Action (attack/thwart): Remove 1 [per_hero] threat from each scheme. Deal 1 [per_hero] damage to each enemy.
#
# CARTES DE REFERENCE
#  - `dr006` Awaken Nature : « each enemy / each scheme », `SetLabel('attack', 'thwart')`, `RemoveThreatFromSchemes` (et non `RemoveThreat`).
#  - `08018` Spycraft : `SetPlay(only_if_you_control_..)` pour « play only if you control » ; ici `only_if_you_control_face=CardFinder(name=..)`.
#  - `Worlds.GetPlayerNumIcon(effect)` : la valeur de l'icone [per_hero] (nombre de joueurs).
#
# TEXTE CONTRE CODE
#  « Play only if you control the Slayer Scythe » -> condition de JEU, pas d'effet. « each scheme » -> principale ET annexes.
#  « each enemy » -> vilain ET sbires. Menace d'abord, puis degats (ordre imprime). 1 [per_hero] = 1 x nombre de joueurs.


def GetAbilities() -> Sequence['Ability']:

    def crimson_scythe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        valeur = Worlds.GetPlayerNumIcon(effect)
        manigances = list(Worlds.FindCardsOnField(effect, card_type=Scheme2))
        if manigances:
            this.RemoveThreatFromSchemes(manigances, valeur, effect)
        ennemis = list(Worlds.GetOnFieldEnemies(effect))
        if ennemis:
            this.DealDamage(ennemis, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            crimson_scythe,
        ).SetPlay(only_if_you_control_face=CardFinder(name=NOM_SLAYER_SCYTHE)).SetLabel('attack', 'thwart'),
    ]
