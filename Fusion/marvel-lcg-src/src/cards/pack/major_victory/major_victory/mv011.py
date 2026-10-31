from . import *

# * Nikki (Nicholette Gold) — ALLIEE, cout 3, [wild]. GUARDIAN. THW 2**, ATK 2*, PV 3.
# [star] Nikki's attacks gain ranged and damage from her attacks can be divided among enemies as you choose.
#
# CARTES DE REFERENCE
#  - `17013` Yondu : `UnitAttackGainKeyword("This", ranged=True)` pour « attacks gain ranged ».
#  - `cd002a` Dagger : `ThisCanAttack(canbe_divided=True)` pour « damage ... may be divided among enemies as you choose ».
#
# TEXTE CONTRE CODE
#  « ranged » -> ignore la riposte ; « divided among enemies as you choose » -> attaque de base repartissable.
#  Les deux phrases portent l'etoile [star] : ce sont deux effets de la meme carte.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            ranged=True,
        ),
        AbilityFactory.ThisCanAttack(
            canbe_divided=True,
        ),
    ]
