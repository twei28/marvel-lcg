from . import *

# * Sn'Tlo — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 4 PV, SCH 2, ATQ 1.
# Reduce the amount of damage Sn'Tlo takes from each attack by 1.
# When Revealed: Heal all damage from Sn'Tlo and put him into play engaged with you.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# « Reduce the amount of damage X takes from each attack by 1 » : **`vision 26015`** Victor Mancha (MEME texte :
# `WhenUnitWouldTakeDamage(NonKeyword, "This", ..., is_from_attack=True)` + `message.ReduceDamage(1, effect)`).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def reduire(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.ReduceDamage(1, effect)

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.NonKeyword, "This", reduire, is_from_attack=True),
    ]
