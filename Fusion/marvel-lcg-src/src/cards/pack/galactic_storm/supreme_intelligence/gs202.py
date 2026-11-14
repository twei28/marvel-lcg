from . import *

# Kree Infantry — SBIRE (Supreme Intelligence), x4. KREE. SCH 1, ATK 2, 5 PV, 1 icone de boost.
# Guard. Patrol.
# When Defeated: Place 2 threat on the main scheme.
#
# Cartes de reference :
#  - **`sm/sandman/27067`** : `WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", op)` = « When Defeated »
#    d'un sbire.
#  - **`50134`** / `ho015` : `PlaceThreatOnSchemes("MainScheme", n, effect)` (litteraux moteur, card_face.py).
#  - Guard / Patrol : bases AUTOMATIQUES (`desc.Guard`, `desc.Patrol`, fiches guard.md / patrol.md).
#
# ⚠ Mots-pieges : « on the MAIN scheme » (pas un complot annexe) ; « 2 threat » (fixe, pas par joueur) ;
# « When Defeated » (vaincu, pas defausse : un sbire Vulnerable defausse par un etourdissement ne la declenche
# pas — Kree Infantry n'est pas Vulnerable).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
