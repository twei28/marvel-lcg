from . import *

# * Ch'Gra — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 2 PV, SCH 1, ATQ 2.
# When Revealed: Heal all damage from Hagar and put him into play engaged with you.
# <b>When Defeated</b>: Flip Queen Veranke.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# « When Defeated: Flip Queen Veranke » : `WhenUnitBeDefeated` (**`44038`**) + `RetournerVeranke` (helper du set, `Card.Flip`).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        RetournerVeranke(effect)

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
