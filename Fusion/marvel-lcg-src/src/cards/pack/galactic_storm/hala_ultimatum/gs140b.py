from . import *

# * Tanalth (III) — MECHANT, stade 3, face B (DISCOVERED). KREE. PV 21[per_hero]. SCH 2. ATK 4.
# Steady.
# When Revealed: Search the encounter deck and discard pile for Grand-High Pursuer and attach it to Tanalth.
# [star] Forced Response: After Tanalth attacks and defeats a character, give her a tough status card and a
#   facedown boost card.
#
# Cartes de reference :
#  - Steady : natif (desc.Steady, fiche mots-cles/steady.md).
#  - « When Revealed: search ... and attach it to Tanalth » : `Search.EncounterCard` + `AttachTo2`
#    (modele `galactic_storm/kree_sentry/__init__.py`, `AttacherUnePoigne`).
#  - Reponse forcee : meme fabrique que gs138b/gs139b, mais la branche « already has » disparait : stade 3
#    donne TOUJOURS les deux a la fois (texte imprime different des stades I/II).


def GetAbilities() -> Sequence['Ability']:
    return CapacitesTanalth(3)
