from . import *
# Outlaw Justice (Aggression, evenement 2 [energy]). ATTACK. THWART. Alliance.
# Hero Action (attack/thwart): Exhaust a STARJAMMER character and a GUARDIAN character → deal X damage among enemies in play and remove
# X threat from among schemes in play, where X is the combined ATK of the two exhausted characters.
#
# Cartes de reference : 48032 Gunboat Diplomacy (MEME structure : `desc.Alliance`, `CostFunc.Exhaust(Select.Alliance([T1, T2]))`, X relu
# sur les cartes inclinees `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`, repartition par deux `ChooseAbilities` a
# `repeat_rules="Threat"` / `"Health"`) ; 23032 As One! (X = somme des `face.attack`). Ici X = ATQ cumulee (pas CTR).
# « among enemies in play » / « among schemes in play » : repartition LIBRE entre tous les ennemis / toutes les manigances (0 a X choix).
def GetAbilities() -> Sequence['Ability']:
    def outlaw_justice(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        initiator = effect.GetInitiator()
        x = 0
        for face in effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards:
            if HasAttack.IsType(face):
                x += face.attack
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "",
                lambda targets:
                    this.RemoveThreatFromSchemes(targets, 1, effect)
            ).SetLabel('thwart')
            .SetTarget(Scheme2, range=(0, x), repeat_rules="Threat")
        )
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "",
                lambda targets:
                    this.DealDamage(targets, 1, effect)
            ).SetLabel('attack')
            .SetTarget(Enemy, range=(0, x), repeat_rules="Health")
        )
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            outlaw_justice,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetCostFunc(CostFunc.Exhaust(Select.Alliance(["STARJAMMER", "GUARDIAN"])))
        .SetTarget2(Scheme2)
        .SetTarget2(Enemy),
    ]
