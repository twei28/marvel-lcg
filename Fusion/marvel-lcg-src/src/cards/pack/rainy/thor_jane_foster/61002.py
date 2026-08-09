from . import *

# * Odinson — custom "Rainy"
# Multiverse. (mot-clé custom de l'auteur, sans effet moteur : une seule
# version « Multiverse » d'un même personnage par deck — géré par l'unicité.)
# Response: After Odinson attacks, choose a player. Deal 1 damage to each
# minion engaged with that player.

def GetAbilities() -> Sequence['Ability']:

    def odinson(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)

        for target in effect.targets:
            player = target.GetControlByPlayer()
            minions = player.GetEngagedMinions()
            if minions:
                this.DealDamage(minions, 1, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "This",
            odinson,
        ).SetTarget("Players")
    ]
