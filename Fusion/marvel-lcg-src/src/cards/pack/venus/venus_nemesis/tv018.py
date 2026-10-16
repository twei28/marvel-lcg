from . import *

# * Groundchuck-Dirtbag — SBIRE. BRUTE. BULL. MOLE. PV 4, MNG 1, ATQ 3, boost etoile seul.
# Guard. Toughness.
# [star] Boost: Deal this card to the first player as a facedown encounter card.
#
# CARTES DE REFERENCE
#  - `01101` Hydra Mercenary (Guard, aucun script) ; `01076` Luke Cage (Toughness, aucun script) ;
#    `tl015` Karai pour le boost (fabrique `BoostDonnerAuPremierJoueur`).
#
# TEXTE CONTRE CODE
#  ⚠ « Guard » (`desc.Guard = 1`) et « Toughness » (`desc.Toughness = 1`) sont LUS PAR LE MOTEUR :
#    aucun module pour eux (fiches `mots-cles/guard.md`, `toughness.md`). Le seul module est
#    la capacite etoile.
#  ⚠ Pas de « (nemesis minion) » imprime : pas de `desc.Nemesis` (il est dans le set nemesis
#    mais non lie au joueur par le texte).


def GetAbilities() -> Sequence['Ability']:
    return [
        BoostDonnerAuPremierJoueur(),
    ]
