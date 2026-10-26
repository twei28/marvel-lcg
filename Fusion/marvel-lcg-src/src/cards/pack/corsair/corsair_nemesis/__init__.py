from cards.pack import *

# Helpers partages du set « Corsair Nemesis » (Phenexian et Mysteltainn, prefixe `cr`).
# ⚠ Un helper vit ICI, jamais dans le `__init__.py` du pack (NameError avale, lecon hk005).

TRAIT_ELITE = "ELITE"


def JoueursEnOrdre(effect: 'Effect') -> List['Player']:
    return list(Worlds.GetPlayers(effect))


def AlliesEtPersonasDe(joueur: 'Player') -> List['CardFace']:
    """« an ally or PERSONA support they control » : allies et soutiens PERSONA sous le controle du joueur."""
    return [f for f in joueur.GetControlCards() if f.IsInPlay() and (Ally.IsType(f) or (Support.IsType(f) and f.HasTrait("PERSONA")))]


def EstElite(face: 'CardFace') -> bool:
    return Minion.IsType(face) and face.HasTrait(TRAIT_ELITE)
