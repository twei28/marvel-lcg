from . import *

# * Fry'lu — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 3 PV, SCH 1, ATQ 2.
# When Revealed: Heal all damage from Fry'lu and put her into play engaged with you.
# <b>When Defeated</b>: Deal the player who defeated Fry'lu a facedown encounter card.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# « Deal the player who defeated X a facedown encounter card » : **`44038`** Dreadpool (`message.GetKillerPlayer()` +
# `player.DealEncounterCards(1, effect)`) et `21128` Tribute.
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        joueur = message.GetKillerPlayer()
        if joueur is not None:
            joueur.DealEncounterCard(this, effect)

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
