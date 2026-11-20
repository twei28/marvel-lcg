from . import *

# Culling the Damned — MANIGANCE ANNEXE. Boost 2, Acceleration, menace de depart 3[per_hero] (natifs, `desc`).
# Forced Interrupt : After a MYSTIC minion is defeated, place one scorned counter here.
# When Defeated : The player who defeated this side scheme looks at X cards in Damnation, where X is equal to the number of scorned counters here.
# Shuffle each card looked at this way back into its owner's deck.
#
# Cartes de reference : defeated.py `AfterUnitBeDefeated`, `WhenSchemeBeDefeated` (`message.defeating_player`), `RegarderEtRemelanger`, compteur `scorned`
# (fiche compteurs-corrupt-scorned.md).
# ⚠ Mots-pieges : « a MYSTIC minion » : le trait, tous les sbires MYSTIC (quel que soit le joueur qui les bat) ; « THE PLAYER WHO DEFEATED this side
# scheme » : celui qui regarde, pas chaque joueur ; X = les compteurs PRESENTS a la defaite.


def GetAbilities() -> Sequence['Ability']:
    def sbire_mystique_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Unused(message)
        Faces.PlaceCountersOn([effect.this.CastTo(SchemeSide2)], 1, 'scorned', effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = message.defeating_player or JoueursDansLOrdre(effect)[0]
        RegarderEtRemelanger(effect, joueur, effect.this.CastTo(SchemeSide2).GetCounters('scorned'))

    return [
        AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedInterrupt, CardFinder(card_type=Minion, trait="MYSTIC"), sbire_mystique_vaincu),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
