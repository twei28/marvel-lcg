from . import *

# Hypnotic Trance (x3). Attachement PSIONIC SKILL, -1 THW (desc `THW+`). « Attached character cannot attack Selene and cannot defend against
# Selene's attacks. When Revealed : Attach to the ally with the highest remaining hit-point without Hypnotic Trance attached. Otherwise, this
# card gains surge. Hero Action : Spend [mental][mental] resources and remove 1 time counter from Beneath the Sun -> discard this card. »
# Cartes de reference : 04119 Neurological Implants (`AttachToFaceWhenPutIntoPlay(most_remaining_hp, without_another_copy, if_cannot_gain_surge)`),
# hf304 (`UnitCannotDefend`), 40091 / hf110 (`PlayerActionToDiscardThis(HeroAction).SetCost`), 16095 (`CostFunc.Counter` sur une AUTRE carte).
# Icone [mental] = noeuds relies (lue contre rm004, comme hf110). Le coût « remove 1 time counter from Beneath the Sun » est un COUT (avant la
# fleche) : la carte n'est jouable que si le JOUR est la face visible.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Ally), most_remaining_hp=True, without_another_copy=True, if_cannot_gain_surge=True),
        *AbilityFactory.UnitCannotAttackTarget("AttachedAlly", cannot_attack=ChercheurSelene()),
        *AbilityFactory.UnitCannotDefend("AttachedAlly", ChercheurSelene(), cannot_trigger_defense_ability=False),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BB")).SetCostFunc(CoutTempsDuJour()),
    ]
