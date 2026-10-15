from . import *

# Impostor — ATTACHEMENT (Secret Invasion ; MEME carte que sk098 de Skrull Empire). CONDITION.
# Treat attached ally as a SKRULL minion with a blank text box. Attached minion's SCH is equal to its printed THW and
#   it does not take consequential damage.
# When Revealed: Attach to the non-SKRULL ally with the most remaining hit points without Impostor attached. Attached
#   ally engages its controller. Otherwise, the villain schemes.
#
# Cartes de reference : **`sk098`** (meme texte, deja fait et teste : on REUTILISE son code), lui-meme calque sur
# **`36038`** Possessed (`TreatAttachedCardAsMinion(Ally, "Controlled Minion")` + `AttachTo2`).
#
# ⚠ Mots-pieges : voir l'en-tete de `skrull_empire/sk098.py` (« NON-SKRULL ally » : un allie Impostor CAMOUFLAGED est
# SKRULL, donc jamais cible ; « most REMAINING hit points » ; « without Impostor attached » ; « engages its
# CONTROLLER » ; « Otherwise, the villain SCHEMES »). La carte technique `skrull_minion` est partagee.
from cards.pack.skrull_menace.skrull_empire import sk098


def GetAbilities() -> Sequence['Ability']:
    return sk098.GetAbilities()
