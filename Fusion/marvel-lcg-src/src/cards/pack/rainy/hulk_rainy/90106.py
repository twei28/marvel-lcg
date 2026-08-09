from . import *

# Interception

def GetAbilities() -> Sequence['Ability']:

    def interception(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)

        message.CancelAllEffectsAndDiscardIt(effect)

        # La carte coute 0 : toute ressource depensee est un surpaiement.
        paid = effect.GetPaidResources()
        if not (paid.HasColor("Y") or paid.HasColor("R")):
            return
        if effect.targets:
            this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "All",
            interception,
            from_encounter=True,
        ).SetPlay()
        .SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity"))
        # Le schema n'est a designer que si le surpaiement a eu lieu : cible
        # facultative.
        .SetTarget(Scheme2, range=(0, 1)),
    ]
