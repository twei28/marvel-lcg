from . import *

# * Shifting Corridors — VILAIN (face unique, A). LOCATION. SCH 0★ / ATQ 0★ / PV infinis. Stalwart.
# ★ Forced Interrupt : When Shifting Corridors would activate against you, instead remove 1 passage counter from here and reveal the top card of the trap deck.
# If the last passage counter is removed from here, the players lose the game.
#
# Cartes de reference : dazzler/dz006 (`WhenEnemyWouldActivate` + `SetBeInstead` = annuler l'activation, filtre « against YOU » par `message.to_player`),
# web_of_deceit/the_lizard/wd054b (« HIT POINTS ∞ » : PV infinis), skrull_menace/shaper_of_worlds/sk228 (`desc.HP = "INF"`, lu par `can_health.py`),
# game/ability/factory/scheme.py `IfNoThreatHerePlayersWinTheGame` (derniere ressource retiree -> `Worlds.SetGameOver`), web_of_deceit/the_lizard/__init__ (compteur retire).
# ⚠ Mots-pieges : « would activate AGAINST YOU » : une activation contre un joueur precis (pas contre les autres) ; « INSTEAD » : l'activation n'a pas lieu (ni attaque, ni
#  manigance, ni carte de boost) ; « the LAST passage counter » : la defaite est immediate, la carte de piege n'est plus revelee ; « HP ∞ » : desc.HP = INF, la carte
#  ne peut pas etre vaincue par les degats (les degats sont de toute facon convertis en menace par sl038b) ; Stalwart : natif (desc).


def GetAbilities() -> Sequence['Ability']:

    def activer(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this
        joueur = message.to_player
        if joueur is None:
            return
        message.SetBeInstead(effect)
        Faces.RemoveCountersOn([this], 1, 'passage', effect)
        if not Worlds.IsGameOver(effect):
            ReveleDuPaquetPiege(effect, joueur)

    def dernier_passage(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, "This", activer),
        AbilityFactory.WhenTheLastCounterIsRemovedFromHere(AbilityType.NonKeywordBold, 'passage', dernier_passage),
    ]
