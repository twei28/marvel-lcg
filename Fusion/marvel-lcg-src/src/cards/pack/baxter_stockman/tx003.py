from . import *

# * Baxter Stockman (III) — VILAIN, stade 3 (Baxter's Lab 3/22). AERIAL. FLY. GENIUS.
# PV 19[per_hero], SCH 2, ATK 2. Toughness.
# Each SWARM minion gains guard.
# When Revealed: Deal each player 1 facedown encounter card.
# Forced Interrupt: When the villain phase begins, each player resolves the "Special" on the
#   Baxter's Laboratory scheme.
#
# Cartes de reference : `sk091` (sk200) « chaque sbire SKRULL gagne guard » =
# `GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Minion), guard=1)` ; `56138`
# `Utility.DealEachPlayerEncounterCard` pour « deal each player 1 facedown encounter card ».
#
# Mots-pieges : « EACH SWARM minion » (tous les sbires SWARM en jeu, quel que soit le joueur
# engage, y compris ceux de Donatello td016/td017) ; « gains GUARD » (mot-cle chiffre : 1).


def GetAbilities() -> Sequence['Ability']:

    def distribuer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Utility.DealEachPlayerEncounterCard(effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2(TRAIT_SWARM, Minion), guard=1),
        AbilityFactory.WhenThisRevealed(None, distribuer),
        AuDebutDeLaPhaseDuMechant(),
    ]
