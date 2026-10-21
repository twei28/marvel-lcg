from . import *

# * Punisher (I, 1A) — VILAIN. SOLDIER. VIGILANTE. SCH 0, ATQ 1, 16 PV par joueur. Toughness.
# Hero Response : After you attack Punisher, spend 2 resources of any type → flip Target Lock to its DISTRACTED side and
#   discard one non-permanent attachment from Punisher.
#
# Cartes de reference : jigsaw/pu058.py (`PlayerAction... SetCost`), `AfterUnitAttackUnit` (cote joueur : attaquant "You"),
# `RetournerTargetLockVersDistracted` (__init__.py). Toughness : natif.
# ⚠ « one NON-PERMANENT attachment » : les armes (pu093-095), Mexican Standoff ; jamais Target Lock (Permanent) ni
# In the Crosshairs ; le joueur choisit. « spend 2 resources of ANY type » : `Cost("2")`.
# Les quatre faces partagent cette capacite (`ReponseDeHeros` dans __init__ de ce fichier est dans punishment/commun_vilain.py).

from .commun_vilain import ReponseDeHeros

def GetAbilities() -> Sequence['Ability']:
    return [ReponseDeHeros(meme_type=False, carte_de_boost=False)]
