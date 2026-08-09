from cards.pack import *

# `TreatAsMinion` est une fonction de module, pas une methode d'AbilityFactory :
# le `from game.ability.factory import *` de cards/pack/__init__.py ne la
# reexporte PAS. Import explicite obligatoire.
from game.ability.factory.treat import TreatAsMinion

################################################################################
# Set nemesis d'Agent Anti-Venom — custom « DesignHacker ».
#
# Mot-cle maison TRAITOR, defini en toutes lettres sur les deux cartes qui le
# posent : « treat that ally as a minion engaged with its owner. It has 1 SCH,
# a blank printed text box, and does not take consequential damage. »
#
# Le moteur sait deja faire cela (`TreatAsMinion`, game/ability/factory/treat.py,
# utilise par Manipulated Mind 27171 et "Lost" Child 47027), mais uniquement
# depuis un ATTACHEMENT. Ici le declencheur est une capacite : on appelle donc
# la fonction directement, avec la carte-gabarit `aav_traitor_minion`
# (« Traitor Minion ») et un SCH force a 1.
################################################################################

TRAITOR_TEMPLATE = "Traitor Minion"


def _sch_a_un(minion: Any, ally: Any, effect: 'Effect') -> None:
    minion.printed_scheme = 1


def GainTraitor(ally: 'CardFace', effect: 'Effect') -> bool:
    """Transforme un allie en sbire engage avec son proprietaire."""
    player = ally.CastTo(Ally).GetControlByPlayer()
    if player is None:
        return False
    return TreatAsMinion(ally, TRAITOR_TEMPLATE, player, effect, process=_sch_a_un)
