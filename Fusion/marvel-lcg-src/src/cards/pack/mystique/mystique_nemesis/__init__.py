from cards.pack import *
# Helpers partages du set « Mystique Nemesis » (⚠ un helper du __init__ du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
# Meme trio que « Destiny Nemesis » (Mister Sinister, Destiny's Warning, So, What's the Plan?), recopie sous les ids `my`.
NOM_SINISTER = "Mister Sinister"
NOM_WARNING = "Destiny's Warning"


def WarningsEnJeu(effect: 'Effect') -> List['CardFace']:
    """Le complot annexe Destiny's Warning, si elle est en jeu."""
    return Worlds.FindCardsOnField(effect, name=NOM_WARNING)


def SinistersEnJeu(effect: 'Effect') -> List['CardFace']:
    return Worlds.FindCardsOnField(effect, name=NOM_SINISTER, card_type=Minion)


def ActiverSinister(effect: 'Effect', sinister: 'CardFace', joueur: 'Player') -> None:
    """« Mister Sinister activates against you EVEN IF Destiny's Warning is in play » : le drapeau leve l'interdiction (my016) le temps de l'activation."""
    sinister.my_forcer = True
    try:
        sinister.DoActivate(joueur, effect)
    finally:
        sinister.my_forcer = False
