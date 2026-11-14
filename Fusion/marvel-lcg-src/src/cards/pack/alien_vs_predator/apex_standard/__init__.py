from cards.pack import *
from cards.pack.alien_vs_predator.commun import *

# Helpers du set « Apex Standard » (ap201-ap207 ; remplace le Standard dans ce scenario, insert). Masterplan (ap206) et Shadow of the Past
# (ap207) reprennent mot pour mot les cartes du core : `ability_link` 01192 / 01190 (aucun module ici).


def SansDeplacerLeCompteur(effect: 'Effect', action: 'Callable[[], Any]') -> None:
    """« Do not move the active villain counter » : la garde vaut pour l'activation que la carte provoque, puis tombe (si rien ne l'a
    consommee : mechant au stade 3/4, activation empechee...)."""
    GarderLeCompteur(effect)
    try:
        action()
    finally:
        OublierLaGarde(effect)
