from . import *

# Improved Recovery Upgrade

def GetAbilities() -> Sequence['Ability']:

    def improved_recovery_upgrade(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)


    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=4,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            AlterEgo,
            recover=1,
        ),
        # CORRECTIF : le texte impose « exhaust this card → draw 1 card ». Sans
        # CostFunc, la carte piochait a CHAQUE recuperation sans jamais
        # s'incliner. Meme patron que 38018 et 48014.
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            improved_recovery_upgrade,
            powers=["REC"],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

