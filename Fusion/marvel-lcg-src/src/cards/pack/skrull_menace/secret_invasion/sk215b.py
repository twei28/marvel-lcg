from . import *

# * Siri — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 4 PV, SCH 1, ATQ 2.
# Patrol. <i>(While this minion is engaged with you, you cannot thwart the main scheme.)</i>
# When Revealed: Heal all damage from Siri and put her into play engaged with you.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# Patrol : mot-cle natif (desc `Patrol`, fiche mots-cles/patrol.md), aucun script.
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    return [
        *SbireImpostor(),
    ]
