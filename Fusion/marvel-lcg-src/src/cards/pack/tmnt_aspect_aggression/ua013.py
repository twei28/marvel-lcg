from . import *

# Critical Wound — AMELIORATION 1 [energy], aspect Aggression (TMNT Aspects, Inkwire). CONDITION. WOUND.
# Attach to a minion that your hero attacked this turn. If attached to a non-ELITE minion, it gains vulnerable.
# Increase the amount of damage attached minion takes from each attack by 1.
#
# MOT-CLE (fiche lue AVANT le code) : vulnerable — docs/reference/mots-cles/vulnerable.md (compteur
#   `Vulnerable`, `HasVulnerable.GainVulnerable`). Aucune carte du depot ne le DONNAIT : on le pose par
#   `GiveKeywordToAttached(..., apply=...)` (modele `sk093`, `GainCrisis`), retire au depart de la carte.
# CARTES DE REFERENCE
#  - `43012` Puncture Wound : « Attach to an enemy that X attacked this turn » = `CardFinder(card_type=...,
#    check_effect_fn=...)` qui lit `world.stat.this_turn_made_attack` (attaquant, effet, cibles).
#  - `33005` Exploit Weakness : « Increase the amount of damage attached enemy takes from each attack by 1 » =
#    `IncreaseAllDamageUnitTakeBy(NonKeyword, "AttachedEnemy", 1, is_from_attack=True)`.
# TEXTE CONTRE CODE
#  ⚠ « a MINION that YOUR HERO attacked THIS TURN » : sbire seulement (pas le vilain), attaque par le HEROS du
#    joueur (pas un allie), pendant ce tour.
#  ⚠ « non-ELITE » : le vulnerable n'est pas donne a un sbire ELITE ; le +1 degat, lui, s'applique toujours.
#  ⚠ « from EACH ATTACK » : pas les degats hors attaque.


def AttaqueParVotreHeros(effect: 'Effect', face: 'CardFace') -> bool:
    joueur = effect.GetInitiator() or effect.this.GetControlByOrOwner()
    for unite, _, cibles in effect.world.stat.this_turn_made_attack:
        if Hero.IsType(unite) and unite.GetControlByOrOwner() == joueur and face in cibles:
            return True
    return False


def GetAbilities() -> Sequence['Ability']:

    def vulnerable(effect: 'Effect', face: 'CardFace', diff: int) -> None:
        face.GainVulnerable(diff, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion, check_effect_fn=AttaqueParVotreHeros)
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            get_new_value=lambda effect, face, faces: 0 if face.HasTrait("ELITE") else 1,
            apply=vulnerable,
        ),
        AbilityFactory.IncreaseAllDamageUnitTakeBy(
            AbilityType.NonKeyword,
            "AttachedEnemy",
            1,
            is_from_attack=True,
        ),
    ]
