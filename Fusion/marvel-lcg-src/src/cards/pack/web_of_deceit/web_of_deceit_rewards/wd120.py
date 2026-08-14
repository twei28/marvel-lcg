from . import *

# * Arana

def GetAbilities() -> Sequence['Ability']:

    def sortie(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        # « Response: After Arana leaves play, deal 5 damage to an enemy. »
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, 5, effect)

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            sortie
        ).SetTarget(Enemy),
    ]
