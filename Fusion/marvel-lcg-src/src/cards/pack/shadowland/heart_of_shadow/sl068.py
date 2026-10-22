from . import *

# * Retainer — SBIRE. BRUTE. DEMON. HAND. SCH 1 / ATQ 4★ / PV 9, Boost 3.
# [star] Retainer's attacks gain overkill.
# [star] Interrupt : When Retainer attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Retainer gets –3 ATK for this attack.
#
# Cartes de reference : sl058 (`UnitAttackGainKeyword("This", overkill=True)`) et sl057 (`InterruptMoinsATQ`), les memes textes que Krahllak.
# ⚠ Mots-pieges : « Retainer's attacks » = les attaques de CE sbire ; « you may » : facultatif, a la charge du joueur attaque ; « -3 ATK for THIS attack ».


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        InterruptMoinsATQ(),
    ]
