from . import *

# * Arms (Destroyed) — COMPONENT. DESTROYED. TECH.
# Permanent.
# Your [[ATTACK]] events cost 1 additional resource.
#
# Jumelle exacte de `st002b`, trait ATTACK au lieu de THWART : meme helper,
# memes pieges (« events » seulement, « your » = le controleur).


def GetAbilities() -> Sequence['Ability']:
    return [
        VosEvenementsDeTraitCoutentUnDePlus("ATTACK"),
    ]
