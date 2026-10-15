from . import *

# Shapeless Wastes (179) — COMPLOT ANNEXE. Menace 2 (fixe), 3 icones Y. Hinder 2[per_hero].
# Hinder 2[per_hero].
# Forced Response: After an ally or a minion is defeated, if that character has the SKRULL trait, flip
#   the villain. Otherwise, place 1 faith counter on the villain.
#
# Cartes de reference :
#  - Hinder : base AUTOMATIQUE (`desc.Hinder = "2*"`, fiche mots-cles/hinder.md), aucun module.
#  - « After an ally or a minion is defeated » : **`mut_gen/mansion_attack/32128b`** (`CardFinder(card_type=
#    Ally|Minion)`) + `AbilityFactory.AfterUnitBeDefeated(ForcedResponse, finder, op)` (defeated.py:386) ;
#    **`hunting_season/hs222`** pour une Reponse forcee d'un complot annexe sur une carte quelconque.
#
# ⚠ Mots-pieges : « an ALLY OR a MINION » (pas le mechant, pas un heros) ; « if THAT character has the SKRULL
# trait » (le defait, pas le mechant) ; « Otherwise » = les non-Skrull ; « AFTER ... is defeated » (Reponse,
# le personnage a deja quitte le jeu : son trait se lit sur la face) ; Hinder place la menace sur CETTE carte.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        if message.trigger.HasTrait("SKRULL"):
            RetournerLeMechant(effect)
        else:
            PoserFoi(effect, 1)

    return [
        AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, CardFinder(card_type=Ally | Minion), vaincu),
    ]
