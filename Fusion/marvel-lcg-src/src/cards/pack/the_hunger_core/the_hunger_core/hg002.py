from . import *

# * The Hunger Core (II) — Hunger. MECHANT, stade 2. HIVE. COSMIC. PV 15[per_hero]. SCH 2. Pas d'ATK imprime.
# Shielded by the Horde. Rupture 1[per_hero].
# Just a Core 1. Instead of attacking you, deal yourself 1 facedown encounter card.
# When Revealed: Each player places 1 infection counter.
#
# Cartes de reference : identiques a hg001.py (Shielded/Just a Core/Rupture mutualises dans CapacitesDuCoeur).
#  - « When Revealed: Each player places 1 infection counter » : `AbilityFactory.WhenThisRevealed`, modele du
#    compteur Infection, `commun.PoserInfection` sur chaque joueur. Se declenche au stade Expert de depart
#    (mise en place) ET en Deeper Inside (I -> II en Standard) : `AdvanceVillainStage(..., call_reveal=True)`.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        for joueur in Worlds.GetPlayers(effect):
            PoserInfection(effect, joueur, 1)

    return CapacitesDuCoeur(just_a_core=1) + [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
