from cards.pack import *

# ===========================================================================
# Set modulaire SEEDS OF CORRUPTION (Galactic Storm, Kajislav) — gs218-gs221.
# Modulaire par defaut du scenario 5 Supreme Intelligence (retirable / ajoutable
# ailleurs par les regles de personnalisation, insert du scenario). Sept cartes :
# Manipulated Memories x2, Psychic Shackles, Mental Torture x2, Whisper in the
# Mind x2. L'icone de ressource imprimee (trois noeuds relies) est la ressource
# MENTALE (B), verifiee par decoupe contre sk003 Wiccan (RES=B, meme maquette).
# ===========================================================================


def AUneRessourceMentaleImprimee(face: 'CardFace') -> bool:
    """« a card with a printed [mental] resource » : au moins une icone mentale IMPRIMEE (pas un joker)."""
    return FacesCounter.GetPrintedResources([face]).HasColorPrinted("B")
