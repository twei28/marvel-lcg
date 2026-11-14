from cards.pack import *

# ===========================================================================
# Set nemesis « Elektra Nemesis » (Hero Pack officiel MC63) : 63029 Aka, 63030 The Fist Fits in the Hand, 63031 Hand Katana,
# 63032 Hand Blademaster, 63033 Hand Archer. Ajoute le 14/11/2026 depuis les scans mc4db
# (.planning/elektra-iron-fist-scans-mc4db/). Gabarits PROCESSUS-CARTE : docs/packs/elektra_heros.md.
# Cas test_capacites : tools/cas/elektra_nemesis.py (noms prefixes « [elektra_nem] »).
#
# ⚠ L'OBLIGATION 63028 Conditioned by the Hand N'EXISTE PAS AU DEPOT : decision utilisateur du 14/11/2026, on ne la monte
#   pas tant que son scan officiel n'est pas publie (seul un apercu non officiel circule). `obligations` reste vide dans
#   deck/starter/elektra.json, et 63010 Resurrection Altar ne revele rien.
# ⚠ Seul 63029 Aka porte `desc.Nemesis` : c'est la seule carte imprimee « (Elektra's nemesis minion.) » (regle moteur du
#   04/10/2026). Les noms se cherchent SANS l'etoile d'unicite (« Aka »).
# ===========================================================================

TRAIT_MAIN: 'CardFace.TRAITS' = "HAND"
NOM_ELEKTRA = "Elektra Natchios"


def JoueurElektra(effect: 'Effect') -> 'Player|None':
    """« the Elektra Natchios player » : le joueur dont l'identite (l'une ou l'autre face) est Elektra Natchios."""
    for joueur in Worlds.GetPlayers(effect):
        identite = joueur.GetIdentity()
        if identite is not None and identite.IsName(NOM_ELEKTRA, check_all_face=True):
            return joueur
    return None


def MelangerQuandVaincu() -> 'Ability':
    """« When Defeated: Shuffle this card into the encounter deck. » (modele : 50098 Machete)."""
    def melanger(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Faces.ShuffleAllTo([effect.this], "EncounterDeck", effect)
    return AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", melanger)
