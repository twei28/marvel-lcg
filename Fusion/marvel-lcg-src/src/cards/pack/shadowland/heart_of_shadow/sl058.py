from . import *

# * Krahllak (II) — VILAIN, stade II. DEMON. HAND. SCH 2 / ATQ 4★ / PV 21 par joueur.
# Steady. Toughness.
# [star] Krahllak's attacks gain overkill.
# [star] Interrupt : When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
#
# Cartes de reference : ho016 Bullseye (« [star] Bullseye's attack gains piercing and overkill » = `AbilityFactory.UnitAttackGainKeyword("This", overkill=True)`, fiche
# mots-cles/overkill.md), sl057 (l'Interruption). Steady et Toughness sont lus dans `desc` (fiches steady.md et toughness.md) : rien a coder.
# ⚠ Mots-pieges : « Krahllak's attacks » = SES attaques (le vilain), pas celles d'un autre ennemi : `"This"` ; l'overkill vaut pour TOUTES ses attaques.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        InterruptMoinsATQ(),
    ]
