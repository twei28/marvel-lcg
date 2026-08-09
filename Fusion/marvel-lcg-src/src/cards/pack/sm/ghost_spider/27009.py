from . import *

# Web-Bracelet

def GetAbilities() -> Sequence['Ability']:

    def web_bracelet(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)


    return [
        # CORRECTIF : le texte est un « Hero Response ». Type Response nu, la
        # restriction de forme heros n'etait pas appliquee (124 des 134 cartes
        # « Hero Response » du depot utilisent bien AbilityType.HeroResponse).
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.HeroResponse,
            "You",
            Event,
            web_bracelet,
            which_abilities=["Interrupt", "Response"],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .LimitOncePerEvent()
    ]

