from . import *
# Energy Blaster. Amelioration TECH WEAPON, cout 1, Restricted, Uses (3 charge counters).
#
# Hero Action: Exhaust Energy Blaster and remove 1 charge counter from it -> deal 1 damage to an enemy. If this action defeats
# that enemy, resolve the "Special" ability on a card in your hand.
#
# Cartes de reference : us007 (`desc.Uses = "3,charge"` + `CostFunc.Counter("This", 1, 'charge')`, sortie de jeu NATIVE au dernier
# compteur), 16005 Root Stomp (`DealDamage(.., if_this_attack_defeats=..)`).
def GetAbilities() -> Sequence['Ability']:
    def blaster(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        def vaincu(unit: 'Unit2') -> None:
            ResoudreUnSpecialEnMain(joueur, effect)
        this.DealDamage(effect.targets, 1, effect, if_this_attack_defeats=vaincu)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            blaster,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'charge'))
        .SetTarget(Enemy),
    ]
