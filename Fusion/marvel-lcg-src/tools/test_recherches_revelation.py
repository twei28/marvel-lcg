"""La recherche faite par une carte revelee se publie avec son fait (13/10/2026).

Refonte de la phase du mechant, encadre 12 : « recherche : rien trouve » et
« trouve : X, paquet melange ». `PlayerAction.NoterRecherche` note chaque
recherche rencontre sur la revelation EN COURS (la pile de
`_RevelationsEnCours`) ; hors revelation, rien.

    python3.10 tools/test_recherches_revelation.py
"""
import os
import sys

sys.dont_write_bytecode = True  # rien a ecrire dans src/
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, 'src'))

# Amorce : `game.player` seul tombe sur un import circulaire ; `engine` charge
# les modules dans le bon ordre (sans initialiser de partie).
from engine import Engine  # noqa: E402,F401
from game.player.action.player_action import PlayerAction  # noqa: E402


class Face:
    def __init__(self, name):
        self.name = name


class Monde:
    pass


def verifier(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f'ok  {message}')


def main():
    # Hors revelation : rien n'est note, et rien ne casse.
    monde = Monde()
    PlayerAction.NoterRecherche(monde, [Face('Le Fondeur')], fouille_paquet=True)
    verifier(PlayerAction._RevelationsEnCours(monde) == [], 'hors revelation : rien')

    # Pendant une revelation : trouvee, puis rien trouve, dans l'ordre.
    en_cours = {'face': None}
    PlayerAction._RevelationsEnCours(monde).append(en_cours)
    PlayerAction.NoterRecherche(monde, [Face('Le Requin-Tigre')], fouille_paquet=True)
    PlayerAction.NoterRecherche(monde, [], fouille_paquet=False)
    verifier(en_cours.get('recherches') == [
        {'trouve': ['Le Requin-Tigre'], 'paquet': True},
        {'trouve': [], 'paquet': False},
    ], 'pendant une revelation : chaque recherche, trouvee ou non')

    # La revelation imbriquee (au sommet de la pile) recoit la sienne, pas la premiere.
    imbriquee = {'face': None}
    PlayerAction._RevelationsEnCours(monde).append(imbriquee)
    PlayerAction.NoterRecherche(monde, [], fouille_paquet=True)
    verifier(imbriquee.get('recherches') == [{'trouve': [], 'paquet': True}] and len(en_cours['recherches']) == 2,
             'la revelation imbriquee recoit sa propre recherche')
    print('OK : recherches de revelation')


if __name__ == '__main__':
    main()
