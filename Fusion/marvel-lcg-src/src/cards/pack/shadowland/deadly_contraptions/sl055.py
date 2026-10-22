from . import *

# Pressure Plate — TRAITRISE. TRAP! (pas d'icone de boost)
# When Revealed : Choose :
#  • Avoid — Spend [mental][mental] resources.
#  • Disarm — Spend [energy][physical][physical] resources, then search the top 4 cards of your deck for a card and add it to your hand. (Shuffle.)
#  • Trip — Discard cards from the top of the encounter deck until a minion is discarded, then reveal it.
#
# Cartes de reference : sl054 (options payantes), mister_fantastic/mf004 (`Search.PlayerDeckTop` + `GainCard`), punisher_mcdc_2026/locations_the_big_apple/pu032
# (`DiscardEncounterCardsUntil` puis `Reveal`).
# ⚠ Mots-pieges : resources B B / Y R R (eclair = energie, poing = physique, noeuds = mentale) ; « the top 4 cards of YOUR deck » : une carte au choix parmi les 4, puis
#  melange (le moteur melange apres une recherche) ; Trip : jusqu'au PREMIER sbire defausse, revele a CE joueur ; aucun sbire dans le deck : rien n'est revele.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def desarme() -> None:
            carte = Search.PlayerDeckTop(effect, joueur, 4)
            if carte is not None:
                joueur.GainCard(carte, effect)

        def declenche() -> None:
            sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
            if sbire is not None:
                sbire.Reveal(joueur, effect)

        ChoixDePiege(effect, joueur,
                     OptionDePiege(effect, joueur, PIEGE_AVOID, "Spend [mental][mental] resources", lambda: None, cout="BB"),
                     OptionDePiege(effect, joueur, PIEGE_DISARM, "Spend [energy][physical][physical] resources, then search the top 4 cards of your deck for a card and add it to your hand",
                                   desarme, cout="YRR"),
                     OptionDePiege(effect, joueur, PIEGE_TRIP, "Discard cards from the top of the encounter deck until a minion is discarded, then reveal it", declenche))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
