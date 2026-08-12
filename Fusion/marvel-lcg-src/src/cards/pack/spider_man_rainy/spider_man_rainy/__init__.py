from cards.pack import *

# Pack custom « Rainy » — Spider-Man (Peter Parker).
# Mecanique des compteurs toile : « web an enemy » = poser 1 compteur 'web'
# sur cet ennemi, plafond de 3 par ennemi. Le plafond et l'effet des compteurs
# (retrait a l'activation, -1 SCH / -1 ATK par compteur retire) sont portes par
# la carte de regles Impact Webbing (sr012), mise en jeu des le setup.


def Weber(cibles: Sequence['CardFace'], nombre: int, effect: 'Effect') -> None:
    cibles = [x for x in cibles if x]
    if cibles and nombre > 0:
        Faces.PlaceCountersOn(list(cibles), nombre, 'web', effect)


def LimiteDeuxParRound(effect: 'Effect', message: 'Message2') -> bool:
    # « Limit twice per round » : meme montage que Magnetic Deflector (90122),
    # le moteur n'offrant en propre que la limite a 1 par round.
    deja = [x for x in effect.world.stat.once_per_round_effects
            if x.ability is effect.ability]
    return len(deja) < 2
