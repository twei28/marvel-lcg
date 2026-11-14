from . import *

# * Krahllak (III) — VILAIN, stade III. DEMON. HAND. SCH 3 / ATQ 4★ / PV 25 par joueur.
# Retaliate 1. Steady. Toughness.
# [star] Krahllak's attacks gain overkill and piercing.
# [star] Interrupt : When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
#
# Cartes de reference : ho016 Bullseye (`UnitAttackGainKeyword("This", piercing=True, overkill=True)`), sl057 (l'Interruption). Retaliate, Steady et Toughness sont lus dans
# `desc` (fiches retaliate.md, steady.md, toughness.md).
# ⚠ Mots-pieges : « overkill AND piercing » : les DEUX drapeaux, sur toutes ses attaques.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True, overkill=True),
        InterruptMoinsATQ(),
    ]
