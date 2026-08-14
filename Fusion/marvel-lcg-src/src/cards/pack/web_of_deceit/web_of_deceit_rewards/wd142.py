from . import *

# * Black Suit

def GetAbilities() -> Sequence['Ability']:

    def costume(cibles: 'Sequence[CardFace]', effect: 'Effect') -> bool:
        # « Hero Resource: Take 1 damage → generate a [wild] resource.
        # (Limit once per phase.) » Le symbiote donne, mais il se sert.
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        this.DealDamage([joueur.GetIdentity()], 1, effect)
        return True

    return [
        # « Your hero gains the SYMBIOTE trait. »
        *AbilityFactory.GiveKeywordToAttached(
            trait="SYMBIOTE",
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G")
        ).SetCostFunc(CostFunc.Custom(None, costume))
        .LimitOncePerPhase(),
    ]
