from cards.pack import *

# Helpers partages du set « Marvel Girl » (Dipsome, prefixe `rm`).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

NOM_HEROS = "Marvel Girl"
NOM_ALTER_EGO = "Rachel Summers"
