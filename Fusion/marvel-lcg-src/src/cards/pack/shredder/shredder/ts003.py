from . import *

# * Shredder (III) — VILAIN, stade 3. FOOT CLAN. NINJA. MNG 2 / ATQ 3 / PV 16[per_hero].
# Shredder can have up to 4 cloaked status cards.
# When Revealed: Search the encounter deck and discard pile for the Kuro Kabuto
#   attachment and reveal it. (Shuffle.)
# Forced Response: After the villain phase ends, give Shredder 2 cloaked status cards.
#
# Cartes de reference : `ts002` (la recherche) et `ts001` (le Response, avec
# DEUX cartes ici : « 2 cloaked status cards » = deux poses, chacune refusee
# si Shredder est deja au maximum).


def GetAbilities() -> Sequence['Ability']:

    def chercher_casque(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = Worlds.GetFirstPlayer(effect)
        face = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            finder=CardFinder(card_ids=["ts007"]),
        )
        if face:
            face.Reveal(joueur, effect)

    return [
        *CapacitesDeShredder(3, cartes_par_phase=2),
        AbilityFactory.WhenThisRevealed(None, chercher_casque),
    ]
