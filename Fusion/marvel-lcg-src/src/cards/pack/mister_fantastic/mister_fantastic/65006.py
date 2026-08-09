from . import *

# Unstable Uniform — custom « DesignHacker »
# Mister Fantastic gets +1 DEF.
# Hero Response: After you defend against an attack, return the bottommost
# Mister Fantastic card from your discard pile to your hand.

def GetAbilities() -> Sequence['Ability']:

    def unstable_uniform(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        faces = [x for x in initiator.discard_pile.Get(True)
                 if CardFinder(set_name="Mister Fantastic").Check(x)]
        if not faces:
            return
        initiator.GainCard(faces[-1], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Mister Fantastic", card_type=Hero),
            defense=1,
        ),
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "You",
            unstable_uniform,
        ),
    ]
