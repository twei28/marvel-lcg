from ..commun import *
from cards.pack.trors.hawkeye import HAWKEYE_BOW_NAME

# Hawkeye MC×DC 2026 (identite alternative, p283-p284). ⚠ Le dossier porte le nom du set nettoye (`Hawkeye MCDC 2026`).
HAWKEYE_QUIVER_NAME = "Hawkeye's Quiver"


def EnJeu(joueur: 'Player', nom: str) -> 'Upgrade|None':
    """L'amelioration `nom` deja en jeu chez ce joueur (le Arc et le Carquois sont uniques)."""
    return joueur.GetIdentity().GetInventoryDeck().FindCard(name=nom, card_type=Upgrade)
