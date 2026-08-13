from . import *

# Blast Radius

def GetAbilities() -> Sequence['Ability']:

    def blast_radius(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        # « up to 5 » : le joueur declare, comme le fait 42014 pour sa
        # prevention. X est ce que le heros a REELLEMENT encaisse, pas ce qui
        # lui a ete inflige : c'est ce que dit « took this way ».
        value = initiator.DeclareNumber(0, 5)
        avant = hero.health
        this.DealDamage([hero], value, effect)
        pris = avant - hero.health
        if pris > 0:
            this.DealDamage(effect.targets, pris, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            blast_radius
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=("Zero", 3)),
    ]
