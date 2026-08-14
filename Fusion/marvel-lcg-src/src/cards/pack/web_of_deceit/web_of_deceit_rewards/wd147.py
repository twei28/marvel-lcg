from . import *

# Out of Patience

def GetAbilities() -> Sequence['Ability']:

    def cogner(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « Response: After your hero attacks and damages a minion, take 1
        # damage → ready your hero. »
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.DealDamage([joueur.GetIdentity()], 1, effect)
        Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.Response,
            "YourHero",
            Minion,
            cogner
        ).SetPlay(),
    ]
