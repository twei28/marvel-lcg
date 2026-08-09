from . import *

# * Malekith — custom "Rainy" (sbire némésis de Thor Jane Foster)
# [star] Forced Response: After Malekith activates, each player takes
# 1 indirect damage.

def GetAbilities() -> Sequence['Ability']:

    def malekith(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Minion)

        for player in list(effect.world.players):
            if player.is_eliminated:
                continue
            player.GetIdentity().TakeIndirectDamage(this, 1, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            "This",
            malekith,
        )
    ]
