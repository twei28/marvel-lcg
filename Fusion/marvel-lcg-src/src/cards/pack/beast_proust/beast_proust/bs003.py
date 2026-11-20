from . import *

# Ultimate Mutation : AMELIORATION (CONDITION), cout 3, [physical].
# Beast gets +1 DEF and +4 hit points, and his basic attacks gain piercing.
#
# CARTES DE REFERENCE
#  - `04159a` Basic Thwart Upgrade : `*GiveKeywordToAttached(Hero, ..)` pour un bonus continu porte par une amelioration de l'identite ; `health` passe par la branche « ignore_flip » de la fabrique.
#  - `22032` Energy Spear / `nt009` : `UnitAttackGainKeyword("AttachedXxx", piercing=True)` ; `is_basic_attack=True` pour « basic attacks ». Fiche `piercing.md`.
#
# TEXTE CONTRE CODE
#  « BEAST gets » : un nom propre = la forme HEROS seulement (lecon an002 / 06007, RECETTES §3) : `Hero`, pas `"You"`. DEF +1 : forme heros. « +4 hit points » : `health` (valeur d'identite, suit l'upgrade tant qu'elle est
#    attachee). « his BASIC attacks gain piercing » : `is_basic_attack=True`, pas les attaques d'evenement.
#  Chiffres : cout 3, DEF +1, PV +4.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(Hero, defense=1, health=4),
        AbilityFactory.UnitAttackGainKeyword("AttachedHero", piercing=True, is_basic_attack=True),
    ]
