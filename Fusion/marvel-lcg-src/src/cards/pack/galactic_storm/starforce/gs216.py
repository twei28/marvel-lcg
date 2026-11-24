from . import *

# * Ultimus — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 1, ATK 1★, 8 PV, 3 icones de boost.
# Villainous. Victory 1.
# ★ Ultimus's attacks gain overkill.
# While Ultimus is in the victory display, the villain's attacks gain overkill.
#
# Cartes de reference : **`gs215`** Shatterax (meme structure) ; **`27078`** / `ho016` pour
# `UnitAttackGainKeyword("This", overkill=True)`.
#
# ⚠ Mots-pieges : « ULTIMUS's attacks » (en jeu) ; « the VILLAIN's attacks » (en vitrine) ; Overkill : l'exces
# de degats sur un allie va a l'identite de son controleur (fiche overkill.md).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AttaquesDuMechantEnVitrine(overkill=True),
    ]
