from . import *

# Skater Punk (CIVILIAN, INFLUENCED) — Vulnerable : base.
# When Defeated: Deal 3 damage to the defeating player's identity.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetDefeatingPlayer()
        if joueur is not None:
            this.DealDamage([joueur.GetIdentity()], 3, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
