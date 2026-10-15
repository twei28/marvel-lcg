from . import *

# * Asti the All-Seeing — SBIRE (New Revengers). REVENGER. PV 4, MNG 2, ATQ 1, 1 boost.
# Forced Interrupt: When Asti the All-Seeing takes any amount of damage, place 1 absorption counter on it.
# When Defeated: Assign 2 indirect damage among players for each absorption counter on Asti the All-Seeing.
#
# Cartes de reference :
#  - Interruption sur les degats : **`core 01098`** Armored Rhino Suit (`WhenUnitWouldTakeDamage(
#    ForcedInterrupt, ..., fn)`, `at_least_damage=1` par defaut = « any amount ») + `Faces.PlaceCountersOn`.
#  - « assign N indirect damage among players » : **`gmw 16085b`** Museum Ship (`first_player.AssignDamage(
#    units, this, n, effect)`, le premier joueur repartit entre les personnages de tous les joueurs).
#  - When Defeated : `WhenUnitBeDefeated(WhenDefeated, "This", ...)` (guide §3.1).
#
# ⚠ Mots-pieges : « takes ANY AMOUNT of damage » : au moins 1 degat reel (Interruption, avant la pose des
# degats : le coup mortel compte donc) ; « 2 indirect damage FOR EACH absorption counter » (2 x jetons) ;
# « among PLAYERS » : repartis entre les joueurs, decides par le premier joueur ; compteur maison 'absorption'
# declare dans card_face.py ; un coup qui ne fait aucun degat (prevention) ne pose pas de jeton.


def GetAbilities() -> Sequence['Ability']:

    def absorbe(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        Unused(message)
        Faces.PlaceCountersOn([effect.this], 1, 'absorption', effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        this = effect.this.CastTo(Minion)
        degats = 2 * this.GetCounters('absorption')
        if degats <= 0:
            return
        premier = Worlds.GetFirstPlayer(effect)
        unites = [u for joueur in Worlds.GetPlayers(effect) for u in joueur.GetControlCharacters()]
        premier.AssignDamage(unites, this, degats, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", absorbe),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
