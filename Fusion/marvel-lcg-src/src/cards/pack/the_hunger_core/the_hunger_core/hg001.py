from . import *

# * The Hunger Core (I) — Heartbeat. MECHANT, stade 1. HIVE. COSMIC. PV 12[per_hero]. SCH 1. Pas d'ATK imprime.
# Shielded by the Horde. Rupture 1[per_hero].
# Just a Core 1. Instead of attacking you, deal yourself 1 facedown encounter card.
#
# Cartes de reference :
#  - « Shielded by the Horde » : brique commune `AbilityFactory.CannotBeAffectedByPlayerCards`, modele Kree Leader
#    (`galactic_storm/hala_ultimatum/gs138a.py`), fiche mots-cles/shielded-by-the-horde.md.
#  - « Just a Core X » : moitie attaque du modele Kree Leader, `WhenUnitWouldAttack` + `SetBeInstead` +
#    `DealEncounterCards`, fiche mots-cles/just-a-core-x.md.
#  - « Rupture X » : `WhenUnitBeDefeated` filtre par `CardFinder(traits=["METAZOMBIE"], card_type=Villain)`,
#    modele defeated.py, fiche mots-cles/rupture-x.md.
#
# ⚠ Mots-pieges : « against a player in hero form » = verifier `joueur.IsHero()`, pas juste l'existence d'un
# joueur cible ; l'alter-ego n'a rien a coder (regle de base du moteur). Texte identique sur hg001/hg002/hg003,
# seuls PV/SCH/Just a Core changent : voir CapacitesDuCoeur dans le __init__.py du set.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesDuCoeur(just_a_core=1)
