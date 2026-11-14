from . import *

# Yautja Wrist Blades — AMELIORATION, cout 1, [physical]. TECH. WEAPON.
# Predator gains retaliate 1 and his basic attacks gain piercing.
#
# Cartes de reference :
#  - `core/captain_america/03009` Captain America's Shield : `*GiveKeywordToAttached(CardFinder(name="..."), retaliate=1)`
#    (fiche mots-cles/retaliate.md) ;
#  - `UnitAttackGainKeyword(attacker, target, is_basic_attack=True, piercing=True)` (do_attack.py) : « his basic attacks gain
#    piercing » (fiche mots-cles/piercing.md ; `27078`, ho016).
#
# ⚠ Mots-pieges :
#  - « PREDATOR gains » : NOM PROPRE, la face HEROS seulement ; ni Yd'Nar (l'alter-ego ne combat pas), ni un allie.
#  - « his BASIC attacks » : l'attaque de base (pouvoir ATK) ; PAS les attaques d'evenement ni d'amelioration (Plasmacaster,
#    Spine Rip). `is_basic_attack=True`.
#  - Retaliate 1 sans condition (« gains » = tant que la carte est en jeu), et la carte ne se retire qu'a la defausse.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Predator"),
            retaliate=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name="Predator", card_type=Hero),
            is_basic_attack=True,
            piercing=True,
        ),
    ]
