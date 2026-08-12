from . import *

# "It Can't End Like This!" — custom « ekAugust »
# Hero Action (attack/thwart): Deal 1 damage to the villain and remove 1
# threat from the main scheme. If the villain schemed last round, ____.
# Bulle : « Confuse the villain. »
# LENIENT : le moteur n'accepte qu'un seul label ; 'attack' retenu.

def GetAbilities() -> Sequence['Ability']:

    def it_cant_end_like_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 1, effect)
        this.RemoveThreatFromSchemes("MainScheme", 1, effect)

        if VillainSchemedLastRound(effect):
            ResolveBlank(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            it_cant_end_like_this
        ).SetPlay().SetLabel('attack'),
    ]
