from . import *

# Brood Breakout — MANIGANCE ANNEXE. Menace 4 (fixe). Boost 3.
# Forced Response: After a [[XENOMORPH]] minion enters play, give it a tough status card.
# When Revealed: Discard cards from the top of the encounter deck until a [[XENOMORPH]] minion is discarded. Reveal it.
#
# Cartes de reference : 04108 Taskmaster's Training Camp (`AfterCardEnterPlay(ForcedResponse, Minion)` + `GiveStatus("Tough")`) ; 01192
#   (`DiscardEncounterCardsUntil` + `Reveal`).
#
# ⚠ Mots-pieges : le sbire revele par le « When Revealed » entre en jeu APRES la manigance : il recoit sa carte Tenace ; un Alien Scout
#   (XENOMORPH) qui entre en jeu aussi.


def GetAbilities() -> Sequence['Ability']:

    def tenace(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Faces.GiveStatus([message.trigger], "Tough", effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        DefausserJusquAReveler(effect, JoueurDuMessage(message, effect), trait="XENOMORPH", card_type=Minion)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, CardFinder(card_type=Minion, trait="XENOMORPH"), tenace),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
