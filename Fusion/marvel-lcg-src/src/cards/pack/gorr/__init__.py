from cards.pack import *

# =============================================================================
# PACK VILAIN « GORR THE GOD BUTCHER » (set 136, prefixe gb, auteur BLUEHG)
#
# 34 cartes physiques, 26 card_id. Le scenario tient sur TROIS horloges, une
# par compteur maison declare dans `CardFace.COUNTER` :
#
#   `plan`   sur le complot principal 1B : +1 a chaque phase du vilain tant
#            que le vilain est au stade 2 ou 3, et a 3 le complot avance.
#   `timer`  sur l'environnement Godbomb (face A) : les joueurs perdent a 12
#            par joueur.
#   `necro`  sur sa face B, All-Black Necroverse : paliers a 3/6/9 par joueur
#            qui renforcent les ennemis NECROVERSE, defaite a 12 par joueur.
#
# ⚠ L'ENVIRONNEMENT EST UNE SEULE CARTE A DEUX FACES (« gb007a,gb007b » dans
# le `set_aside` du scenario). Le complot 3A la RETOURNE si elle est deja en
# jeu, et ne la sort de la reserve que si elle n'y est pas. Les deux faces ne
# sont donc jamais en jeu ensemble : les helpers ci-dessous cherchent la face
# voulue par son NOM, jamais par son type.
# =============================================================================

NOM_GODBOMB = "Godbomb"
NOM_NECROVERSE = "All-Black Necroverse"
NOM_GORR = "Gorr the God Butcher"


def TrouverGodbomb(effect: 'Effect') -> 'CardFace|None':
    """La face Godbomb, si c'est elle qui est en jeu."""
    return Worlds.FindCardOnField(effect, name=NOM_GODBOMB, card_type=Environment)


def TrouverNecroverse(effect: 'Effect') -> 'CardFace|None':
    """La face All-Black Necroverse, si c'est elle qui est en jeu."""
    return Worlds.FindCardOnField(effect, name=NOM_NECROVERSE, card_type=Environment)


def TrouverGorr(effect: 'Effect') -> 'Villain|None':
    """Le vilain en jeu, quel que soit son stade (I, II ou III)."""
    return Worlds.FindVillain(effect)


def PoserTimer(effect: 'Effect', nombre: 'int|str') -> bool:
    """Pose des compteurs `timer` sur Godbomb. Rend False si elle n'est pas la.

    « place 1 timer counter on the Godbomb environment, if able » : le « if
    able » de Heroes' Labor se lit sur ce retour, il ne se devine pas.
    """
    env = TrouverGodbomb(effect)
    if env is None:
        return False
    Faces.PlaceCountersOn([env], nombre, 'timer', effect)
    return True


def PoserNecro(effect: 'Effect', nombre: 'int|str') -> bool:
    """Pose des compteurs `necro` sur All-Black Necroverse. False si absente."""
    env = TrouverNecroverse(effect)
    if env is None:
        return False
    Faces.PlaceCountersOn([env], nombre, 'necro', effect)
    return True
