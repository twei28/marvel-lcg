from . import *

# hs179 Finish Them Off (Experience Cost 2)
# Hero Action (attack) : 2 degats a un ennemi ; s'il est vaincu ainsi, pioche 2 cartes.

def GetAbilities() -> Sequence['Ability']:

    def achever(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()

        def vaincu(unit: 'Unit2') -> None:
            Unused(unit)
            joueur.DrawUp(2, effect)

        this.DealDamage(effect.targets, 2, effect, if_this_attack_defeats=vaincu)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, achever).SetPlay().SetLabel('attack').SetTarget(Enemy),
    ]
