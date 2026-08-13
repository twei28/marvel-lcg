from . import *

# * Paladin

def GetAbilities() -> Sequence['Ability']:

    def paladin(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        ennemi = message.target
        purples = [f for f in ennemi.GetInventoryDeck().GetAll()
                   if Upgrade.IsType(f) and f.paper.card_class == "Determination"]
        if purples:
            message.would_atk_message.GiveBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            "This",
            Enemy,
            paladin,
        ),
    ]
