from . import *

# The Life Stealer — Manigance annexe, menace de depart 2, Boost 2.
# All friendly characters get -1 ATK.
# When Revealed: Place 1 additional threat here for each friendly character in play.
#
# Cartes de reference :
#  - `ho015` / `RECETTES-MOTEUR` §3 : bonus continu sur d'autres cartes par `*GiveKeywordToInPlayWhenApplyThis(
#    finder, attack=N)` (rend une LISTE).
#  - `50134` / `wd` : `WhenThisRevealed(None, op)` + `this.PlaceThreatOnSchemes([this], n, effect)`.
#
# ⚠ Mots-pieges :
#  - « friendly characters » = les IDENTITES (heros ou alter-ego) et les ALLIES de tous les joueurs (classe
#    `Friend`), jamais les ennemis.
#  - « ADDITIONAL threat » : s'ajoute aux 2 menaces imprimees (`StartingThreat`).
#  - « for each friendly character IN PLAY » : compte a la REVELATION ; il ne se met pas a jour ensuite.
#  - « -1 ATK » : continu tant que la manigance est en jeu.


def GetAbilities() -> Sequence['Ability']:

    def voler_la_vie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)

        nombre = len(Worlds.FindCardsOnField(effect, card_type=Friend))
        if nombre > 0:
            this.PlaceThreatOnSchemes([this], nombre, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Friend),
            attack=-1,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            voler_la_vie,
        ),
    ]
