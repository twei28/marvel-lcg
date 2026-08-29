from . import *

# Dora Milaje — CREATED ALLY, jamais dans un deck
# Fragile. (Attacks against this character gain overkill.)
# Legion. (2 allies with the legion keyword count as 1 ally toward your ally
#   limit.)
#
# Jeton "Created Ally" cree par Adored Ones (ok004/ok005) via
# `CreerJetonEtMettreEnJeu` (okoye/__init__.py) -- jamais liste dans un
# hero_deck, comme les artefacts mk021-024 de moon_knight. `Fragile()` et
# `Legion()` sont definis une seule fois dans okoye/__init__.py (les DEUX
# seuls porteurs de ces mots-cles dans ce pack).


def GetAbilities() -> Sequence['Ability']:

    return [
        Fragile(),
        Legion(),
    ]
