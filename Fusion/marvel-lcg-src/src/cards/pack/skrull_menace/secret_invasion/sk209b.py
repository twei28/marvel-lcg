from . import *

# * Khn'nr — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 3 PV, SCH 1, ATQ 2.
# When Revealed: Heal all damage from Khn'nr and put him into play engaged with you.
# <b>When Defeated</b>: Remove all suspicion counters from "Who Do You Trust?".
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# When Defeated : **`WhenUnitBeDefeated(WhenDefeated, "This", ...)`** (`44038` Dreadpool, `sk189b` Queen Veranke).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        RetirerSoupcons(effect, "All")

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
