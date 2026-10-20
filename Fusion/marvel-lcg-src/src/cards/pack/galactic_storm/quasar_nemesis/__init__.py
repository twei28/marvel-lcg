from cards.pack import *

# Set « Quasar Nemesis » (Galactic Storm, Kajislav) : gs099q Maelstrom,
# gs239q Entropy Ascendant, gs237q Avatar of Oblivion, gs240q Distant
# Manipulation (x2). Les helpers des Quantum Bands vivent dans le set du heros.
from cards.pack.galactic_storm.quasar import NOM_BANDES, EstLesBandes, JoueurDeCetteCarte


def JoueurQuasar(effect: 'Effect', bandes: 'CardFace|None') -> 'Player|None':
    """« the Quasar player » : le joueur dont l'identite est Quasar / Wendell
    Vaughn (gs300a/gs300b) ; a defaut, le proprietaire des Bandes."""
    for joueur in effect.world.const_players:
        identite = joueur.GetIdentity()
        if identite is not None and str(getattr(identite.paper, "card_id", "")).startswith("gs300"):
            if not joueur.is_eliminated:
                return joueur
    if bandes is not None:
        proprietaire = bandes.GetOwner()
        if Player.IsType(proprietaire):
            return proprietaire
    return None
