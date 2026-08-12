from . import *

# Unstable Uniform — custom « DesignHacker »
# The Thing gets +1 DEF.
# Hero Response: After you defend against an attack, draw a card.

def GetAbilities() -> Sequence['Ability']:

    def unstable_uniform(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="The Thing", card_type=Hero),
            defense=1,
        ),
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "You",
            unstable_uniform,
        ),
    ]
