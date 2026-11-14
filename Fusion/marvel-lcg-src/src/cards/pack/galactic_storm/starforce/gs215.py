from . import *

# * Shatterax — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 1, ATK 1★, 8 PV, 3 icones de boost.
# Villainous. Victory 1.
# ★ Shatterax's attacks gain piercing.
# While Shatterax is in the victory display, the villain's attacks gain piercing.
#
# Cartes de reference :
#  - **`27078`** / `ho016` : `UnitAttackGainKeyword("This", piercing=True)` = « X's attacks gain piercing »
#    (`attacker="This"` pour ne pas toucher un homonyme).
#  - « While ... in the victory display, the villain's attacks gain piercing » : `AttaquesDuMechantEnVitrine`
#    du set (`UnitAttackGainKeyword(Villain, ...).NoOutOfPlayLimit()`, condition « en vitrine »).
#
# ⚠ Mots-pieges : « SHATTERAX's attacks » (les siennes, en jeu) ; « the VILLAIN's attacks » (en vitrine,
# toutes les attaques du mechant) ; Piercing : defausse les cartes Tenace du personnage attaque avant les
# degats (fiche piercing.md).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AttaquesDuMechantEnVitrine(piercing=True),
    ]
