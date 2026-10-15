from . import *

# * Dharr — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 3 PV, SCH 2, ATQ 1.
# Villainous. <i>(When this minion activates, give it a boost card.)</i>
# When Revealed: Heal all damage from Dharr and put him into play engaged with you.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# Villainous : mot-cle natif (desc `Villainous`, fiche mots-cles/villainous.md), aucun script.
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    return [
        *SbireImpostor(),
    ]
