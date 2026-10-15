from . import *

# Fulfill the Prophecy — COMPLOT ANNEXE (Secret Invasion). Menace 3, Hinder 1[per_hero], icone ACCELERATION, 2 boosts.
# Hinder 1[per_hero].
# Each SKRULL minion gains guard and patrol.
#
# Cartes de reference : **`skrull_empire/sk091`** Satriani (`GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Minion),
# guard=1)`, avec `patrol=1` en plus) ; Hinder : mot-cle natif (desc `Hinder`, fiche mots-cles/hinder.md).
#
# ⚠ Mots-pieges : « EACH SKRULL MINION » (le mechant Veranke n'est pas un sbire) ; « guard AND patrol » : les deux mots-cles,
# valeur 1 ; « gains » : tant que le complot annexe est en jeu.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Minion), guard=1, patrol=1),
    ]
