from . import *

# * Iron Monk — SBIRE. HAND. MYSTIC. Patrol. Toughness. SCH 2 / ATQ 1 / PV 4, Boost 2.
# While Iron Monk is engaged with you, you cannot choose the "Avoid" effect on TRAP! cards.
#
# Cartes de reference : game/ability/factory/player.py `PlayersCannotThwartWhile` (capacite continue qui repond a une question « CheckIf... » du moteur), `PeutChoisirUnEffetDePiege`
# (ce module : la question posee par `ChoixDePiege` avant d'offrir une option), patrol.md / toughness.md (natifs).
# ⚠ Mots-pieges : « engaged with YOU » : seulement le joueur avec qui Iron Monk est engage (un autre joueur peut toujours choisir Avoid) ; « Avoid » seulement (Disarm et Trip
#  restent permis) ; « TRAP! cards » : tous les pieges ; Patrol et Toughness : natifs (desc).


def GetAbilities() -> Sequence['Ability']:

    def engage_avec_lui(effect: 'Effect', message: 'PeutChoisirUnEffetDePiege') -> bool:
        this = effect.this.CastTo(Minion)
        return message.effet == PIEGE_AVOID and this.IsInPlay() and this.GetEngagedPlayer() is message.joueur

    return [
        Ability(AbilityType.NonKeyword, PeutChoisirUnEffetDePiege, [engage_avec_lui], lambda effect, message: message.Interdire(effect)),
    ]
