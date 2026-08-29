from . import *

# Midnight Angel — CREATED ALLY, AERIAL. DORA MILAJE. WAKANDA, jamais dans un
#   deck
# Fragile. (Attacks against this character gain overkill.)
# Legion. (2 allies with the legion keyword count as 1 ally toward your ally
#   limit.)
#
# Jeton "Created Ally" cree par Angelic Warfare (ok006/ok007), meme modele
# que ok017 (Dora Milaje).


def GetAbilities() -> Sequence['Ability']:

    return [
        Fragile(),
        Legion(),
    ]
