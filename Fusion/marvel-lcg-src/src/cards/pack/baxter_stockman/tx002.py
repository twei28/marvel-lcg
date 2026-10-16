from . import *

# * Baxter Stockman (II) — VILAIN, stade 2 (Baxter's Lab 2/22). AERIAL. FLY. GENIUS.
# PV 16[per_hero], SCH 2, ATK 1. Toughness.
# When Revealed: Search the encounter deck and discard pile for the Baxter Blaster attachment and
#   reveal it. (Shuffle.)
# Forced Interrupt: When the villain phase begins, each player resolves the "Special" on the
#   Baxter's Laboratory scheme.
#
# Cartes de reference : `sk142` Paibok II (`ChercherEtReveler` : `Search.EncounterCard(
# include_discard_pile=True)` + `face.Reveal`) ; le melange est le comportement natif de la fouille.
#
# Mots-pieges : « the encounter deck AND DISCARD PILE » (pas la partie : une Blaster deja en jeu
# n'est pas re-revelee) ; « the Baxter Blaster attachment » = tx005 par card_id.


def GetAbilities() -> Sequence['Ability']:

    def chercher_le_blaster(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer() or Worlds.GetFirstPlayer(effect)
        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            finder=CardFinder(card_ids=["tx005"], card_type=Attachment),
        )
        if face is not None:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, chercher_le_blaster),
        AuDebutDeLaPhaseDuMechant(),
    ]
