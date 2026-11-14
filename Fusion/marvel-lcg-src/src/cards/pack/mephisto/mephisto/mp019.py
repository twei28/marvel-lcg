from . import *

# Hotel Inferno — MANIGANCE ANNEXE. Boost 1, Acceleration, menace de depart 2[per_hero] (natifs, `desc`).
# When Revealed : Place 6 threat on the main scheme for every 6 cards in Damnation.
# When Defeated : The player who defeated this scheme looks at up to 6 cards in Damnation. Shuffle each card looked at this way back into its owner's deck.
#
# Cartes de reference : mp016/mp017 (`WhenSchemeBeDefeated`, `RegarderEtRemelanger`), `WhenThisRevealed` (mp002), `PlaceThreatOnSchemes` (mp001).
# ⚠ Mots-pieges : « for EVERY 6 cards » : division entiere (5 cartes = 0, 12 = 12 menaces), toutes piles confondues ; « UP TO 6 » : le joueur peut
# s'arreter avant (`au_plus`) ; « THE PLAYER WHO DEFEATED » : un seul joueur.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        menace = 6 * (len(ToutesLesDamnations(effect)) // 6)
        if menace > 0:
            effect.this.PlaceThreatOnSchemes("MainScheme", menace, effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = message.defeating_player or JoueursDansLOrdre(effect)[0]
        RegarderEtRemelanger(effect, joueur, 6, au_plus=True)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
