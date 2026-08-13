from . import *

# Flummoxed

def GetAbilities() -> Sequence['Ability']:

    def check_moitie(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        identity = effect.GetInitiator().GetIdentity()
        return identity.health < identity.max_health/2

    return [
        AbilityFactory.ReduceCostToPlayThis(
            1,
            conditions=[check_moitie]
        ),
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally|Minion, non_trait="ELITE")
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            treat_as_blank=True,
        ),
    ]
