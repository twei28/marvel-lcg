from . import *

# Mutant Hunting Season (1B) — COMPLOT PRINCIPAL, stade 1B. Menace cible 9 par joueur, +1 par joueur par round, depart 1 par joueur.
# Forced Response: After a player deck empties, place an acceleration token here.
# If this scheme is completed, the players lose the game.
#
# Cartes de reference :
#  - valeurs « N par joueur » : `01097b` Rhino (`StartingThreat`, `TargetThreat`, `EscalationThreat` en `"N*"`).
#  - « After a deck runs out » : `AfterDeckRunOut` (`sk288`, `ch002` Shang-Chi) ; ici N IMPORTE QUEL deck de joueur, donc `Ability(...)`
#    construit a la main (la fabrique compare a UN deck) ; `scheme.PlaceAccelerationToken(n, effect)` (`56167`).
#
# ⚠ Mots-pieges :
#  - « a PLAYER deck » : le deck de n'importe quel joueur, pas seulement le premier ; le deck de rencontre ne compte pas ;
#  - le jeton d'acceleration se pose SUR CE complot et s'ajoute a l'escalade du round ;
#  - « If completed, the players lose » : defaite native des complots principaux (rien a coder).


def GetAbilities() -> Sequence['Ability']:

    def acceleration(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(message)

        this.PlaceAccelerationToken(1, effect)

    def deck_de_joueur(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> bool:
        Unused(effect)
        return bool(message.deck.flags.is_player_deck)

    return [
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterDeckRunOut,
            [deck_de_joueur],
            acceleration,
        ),
    ]
