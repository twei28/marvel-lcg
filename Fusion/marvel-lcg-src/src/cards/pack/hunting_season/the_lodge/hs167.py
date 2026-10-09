from . import *

# hs167 * Ka-Zar (Experience Cost 4)
# Response : apres son entree en jeu, inflige au vilain des degats egaux a son numero d'etape.

def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        for vilain in effect.targets:
            this.DealDamage([vilain], vilain.printed_stage, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", frapper).SetTarget(Villain),
    ]
