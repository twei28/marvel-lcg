from . import *

# Hulk Smash

def GetAbilities() -> Sequence['Ability']:

    def hulk_smash(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        # Trois attaques distinctes contre la meme cible.
        for _ in range(3):
            hero.DealDamage(effect.targets, 3, effect, property=AttackProperty())

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hulk_smash
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
