from cards.pack import *

# Helpers partages du set « Marvel Girl Nemesis » (Dipsome, prefixe `rm`).
# ⚠ Un helper vit ICI, jamais dans le `__init__.py` du pack (NameError avale, lecon hk005).

NOM_HEROS = "Marvel Girl"


def EstMarvelGirl(joueur: 'Player|None') -> bool:
    """Vrai quand l'identite du joueur est Marvel Girl en forme HEROS (« After Marvel Girl's turn begins »)."""
    if joueur is None:
        return False
    identite = joueur.GetIdentity()
    return identite is not None and Hero.IsType(identite) and identite.IsName(NOM_HEROS)
