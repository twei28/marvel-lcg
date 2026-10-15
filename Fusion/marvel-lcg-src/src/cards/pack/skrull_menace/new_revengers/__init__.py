from cards.pack import *

# ===========================================================================
# Set modulaire NEW REVENGERS (Skrull Menace, Kajislav) — sk161-169.
# Livre avec le scenario Paibok ; l'insert p.12 le dit RETIRABLE du scenario et
# AJOUTABLE a d'autres : aucun texte ne doit donc supposer Paibok. Tout ce qui
# parle du « villain » vise le mechant COURANT, quel qu'il soit.
# Trait maison REVENGER (card_face.py) : porte par sept cartes du set, et donne
# AU MECHANT par The Revenge Time (sk168).
# ===========================================================================

TRAIT_REVENGER = "REVENGER"


def EnnemisRevenger(effect: 'Effect') -> List['CardFace']:
    """Les ENNEMIS (sbires, mechant, ...) en jeu qui portent le trait REVENGER. Le mechant en fait
    partie une fois que The Revenge Time (sk168) lui a donne le trait."""
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Enemy.IsType(f) and f.IsInPlay() and f.HasTrait(TRAIT_REVENGER)]


def AutreEnnemiRevenger(effect: 'Effect', *args: Any) -> bool:
    """« another REVENGER enemy is in play » : un ennemi REVENGER AUTRE que la carte qui porte la
    capacite (The Maker est lui-meme un Revenger)."""
    Unused(args)
    this = effect.this
    return any(f.card != this.card for f in EnnemisRevenger(effect))


def ChercherEtReveler(effect: 'Effect', joueur: 'Player|None', **filtre: Any) -> 'CardFace|None':
    """« Search the encounter deck and discard pile for X and reveal it. » (La fouille melange le
    deck rencontre, comportement natif.) Modele 01136 Ultron."""
    face = Search.EncounterCard(effect, include_discard_pile=True, **filtre)
    if face is not None:
        face.Reveal(joueur or Worlds.GetFirstPlayer(effect), effect)
    return face
