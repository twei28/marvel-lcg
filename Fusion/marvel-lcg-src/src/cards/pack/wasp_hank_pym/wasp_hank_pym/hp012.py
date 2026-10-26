from . import *
# * The Stinger — amelioration. Hero Action (attack) : incline -> X degats repartis entre les ennemis de ton choix,
# X = nombre de changements de forme ce tour. Un degat par designation (comme 13006 Wasp Sting) ; CORRECTIF 26/10/2026 :
# exactement X designations (« deal X damage » oblige a les infliger tous : le joueur ne peut plus en designer moins).
def GetAbilities() -> Sequence['Ability']:
    def stinger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        x = formes_changees_ce_tour(effect)
        this.DealDamage(list(effect.targets)[:x], 1, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stinger,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy, range=formes_changees_ce_tour, repeat_rules="Health"),
    ]
