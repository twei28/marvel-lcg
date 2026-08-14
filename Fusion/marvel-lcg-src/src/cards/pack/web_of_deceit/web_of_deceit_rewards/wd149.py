from . import *

# Monstrous

def GetAbilities() -> Sequence['Ability']:

    def rage(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        # « Hero Response: After you spend this card, deal 3 damage to the
        # villain. Then, place 3 threat on a scheme. »
        this = effect.this.CastTo(Resource)
        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 3, effect)
        this.PlaceThreatOnSchemes(effect.targets, 3, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            rage
        ).SetTarget(Scheme2),
    ]
