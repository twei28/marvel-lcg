from . import *

# Hand Archer — SBIRE, HAND. PV 3, ATQ 1*, MAN 1, 1 icone de boost. Quickstrike (desc). Nemesis 5/5.
# [star] Ses attaques gagnent ranged. When Defeated : se melange dans le paquet de rencontre.
#
# CARTES DE REFERENCE : `50098` Machete (`UnitAttackGainKeyword("This", piercing=True)` ; ici `ranged=True`).
# ⚠ Ranged n'a pas de cle `desc` : il passe par `UnitAttackGainKeyword` (riposte ignoree).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword("This", ranged=True),
        MelangerQuandVaincu(),
    ]
