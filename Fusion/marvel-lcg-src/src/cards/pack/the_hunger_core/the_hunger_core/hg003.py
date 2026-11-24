from . import *

# * The Hunger Core (III) — Hive. MECHANT, stade 3. HIVE. COSMIC. PV 18[per_hero]. SCH 3. Pas d'ATK imprime. Steady.
# Shielded by the Horde. Rupture 1[per_hero]. Steady.
# Just a Core 2. Instead of attacking you, deal yourself 2 facedown encounter cards.
# When Revealed: Each player places 1 infection counter.
#
# Cartes de reference : identiques a hg001.py/hg002.py. Seul changement de fond : Just a Core PASSE A 2.
# « Steady » est lu nativement par le moteur depuis `desc.Steady` (fiche mots-cles/steady.md) : aucun code ici.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        for joueur in Worlds.GetPlayers(effect):
            PoserInfection(effect, joueur, 1)

    return CapacitesDuCoeur(just_a_core=2) + [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
