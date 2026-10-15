from . import *

# * H'kurrek — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 2 PV, SCH 1, ATQ 2.
# [star] H'kurrek's attacks gain overkill, piercing, and ranged.
# When Revealed: Heal all damage from H'kurrek and put him into play engaged with you.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# ★ « X's attacks gain overkill, piercing, and ranged » : **`next_evol 40107`** Favored Weapon (`UnitAttackGainKeyword`
# avec les trois mots-cles) ; **`sk162`** pour `ranged=True`.
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    return [
        *SbireImpostor(),
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True, piercing=True, ranged=True),
    ]
