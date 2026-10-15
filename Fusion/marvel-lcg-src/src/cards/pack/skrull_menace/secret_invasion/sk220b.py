from . import *

# * Hs'fld — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 3 PV, SCH 1, ATQ 2.
# When Revealed: Heal all damage from Hs'fld and put him into play engaged with you.
# <b>When Defeated</b>: The player who defeated Hs'fld puts a [[CAMOUFLAGED]] ally at random from the [[IMPOSTOR]] deck into play under their control.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# « The player who defeated X puts a CAMOUFLAGED ally at random from the IMPOSTOR deck into play under their control » :
# `WhenUnitBeDefeated` + `message.GetKillerPlayer()` (**`44038`**) puis `MettreAllieCamoufle` (helper du set).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.GetKillerPlayer()
        if joueur is not None:
            MettreAllieCamoufle(effect, joueur)

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
