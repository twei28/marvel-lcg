from cards.pack import *

# ===========================================================================
# Modulaire ACCUSER CORPS (Galactic Storm, Kajislav). Cartes gs156-gs160, numeros imprimes 156-160
# (livret 1.2 : regles mentionnees seulement comme modulaire activable/retirable par les regles de
# personnalisation, p.14, aucun insert dedie).
# ===========================================================================


def LeVilain(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindVillain(effect)


def JoueurVise(effect: 'Effect', message: 'Any') -> 'Player|None':
    """Le « vous » d'un Boost : le joueur attaque, sinon l'initiateur de l'effet (convention GS4 :
    `message.against_player` suit le controleur attaque)."""
    joueur = getattr(message, 'against_player', None)
    return joueur or effect.GetInitiator()
