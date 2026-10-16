from . import *

# * Shredder (II) — VILAIN, stade 2. FOOT CLAN. NINJA. MNG 2 / ATQ 2 / PV 14[per_hero].
# Shredder can have up to 3 cloaked status cards.
# When Revealed: Search the encounter deck and discard pile for the Bladed Armor
#   attachment and reveal it. (Shuffle.)
# Forced Response: After the villain phase ends, give Shredder a cloaked status card.
#
# Cartes de reference : `01095` (Rhino II : « Search the encounter deck and
# discard pile for X and reveal it », `Search.EncounterCard(include_discard_pile=
# True, ...)` puis `Reveal`) et `ts001` pour le reste. Bladed Armor est
# cherchee par card_id (`ts006`), jamais par le nom.


def GetAbilities() -> Sequence['Ability']:

    def chercher_armure(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = Worlds.GetFirstPlayer(effect)
        face = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            finder=CardFinder(card_ids=["ts006"]),
        )
        if face:
            face.Reveal(joueur, effect)

    return [
        *CapacitesDeShredder(2),
        AbilityFactory.WhenThisRevealed(None, chercher_armure),
    ]
