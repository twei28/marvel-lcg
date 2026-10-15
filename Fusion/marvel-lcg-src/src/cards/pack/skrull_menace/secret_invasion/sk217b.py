from . import *
from game.ability.factory.additional_cost import CostFunction

# * De'Lila — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 3 PV, SCH 2, ATQ 1.
# As an additional cost to attack De'Lila, you must spend 1 resource of any type.
# When Revealed: Heal all damage from De'Lila and put her into play engaged with you.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# « As an additional cost to attack X, you must spend 1 resource of any type » : **`sk123`** Invisibility (MEME texte pour
# Super-Skrull : `WhenUnitWouldBeAttacked` + `CostFunction(...CostFunc.Spend(Cost("1")))`), et `58027` Brother vs. Brother.
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def payer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        CostFunction(effect, message.attacker, message, CostFunc.Spend(Cost("1")))

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitWouldBeAttacked(AbilityType.NonKeyword, "This", payer),
    ]
