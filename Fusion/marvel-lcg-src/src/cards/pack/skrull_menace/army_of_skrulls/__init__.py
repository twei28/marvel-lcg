from cards.pack import *

# ===========================================================================
# Set modulaire ARMY OF SKRULLS (Skrull Menace, Kajislav) — sk113-116.
# Livre avec le scenario Skrull Empire, jouable avec n'importe quel mechant.
# ===========================================================================


def EnnemisSkrullEnJeu(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Enemy.IsType(f) and f.IsInPlay() and f.HasTrait("SKRULL")]
