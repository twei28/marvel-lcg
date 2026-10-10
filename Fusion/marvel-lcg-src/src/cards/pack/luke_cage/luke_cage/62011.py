from . import *
def GetAbilities() -> Sequence['Ability']:
    def power_man(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        effect.GetInitiator().DrawUp(1, effect)
    return [
        # CORRECTIF (10/10/2026, rapport n73) : « After a tough status card is
        # discarded from LUKE CAGE ». `"This"` visait Power Man lui-meme (et
        # rendait l'aptitude locale) : elle ne partait jamais. Modele : 32006
        # Organic Steel, meme phrase pour Colossus.
        AbilityFactory.AfterStatusDiscardFrom(AbilityType.HeroResponse, CardFinder(name="Luke Cage"), "Tough", power_man)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
