from . import *

# * Man-Thing (Theodore Sallis) — DEFENDER. PSIONIC — allie, cout 4
# Toughness.
# Reduce the cost to play Man-Thing by 1 for each Howard the Duck side scheme
#   in the victory display.
#
# « Toughness » est un mot-cle AUTOMATIQUE, lu par le moteur directement dans
# `desc.Toughness` (PROCESSUS-CARTE etape 5, « bases automatiques a ne pas
# recoder ») : aucune ability a ecrire.
#
# Reduction de cout : modele exact phoenix/34021.py (Storm),
# `AbilityFactory.ReduceCostToPlayThis(<fn>)`. La fonction rend le MONTANT de
# la reduction (resources.py:586-637, `update_cost_fn` est multiplie par un
# `base_val` de 1 puis nie) : ici le nombre de manigances annexes DE HOWARD
# dans la zone de victoire — pas toutes les manigances annexes, voir les deux
# portees documentees dans le __init__.py du set.


def GetAbilities() -> Sequence['Ability']:

    def reduction(effect: 'Effect') -> int:
        return NombreDeManigancesHowardEnVictoire(effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(reduction),
    ]
