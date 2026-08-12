from . import *

# Unstable Uniform — custom « DesignHacker »
# Human Torch gets +1 DEF.
# Hero Response: After you take damage from an attack, place a flame counter
# on the attacker.

def GetAbilities() -> Sequence['Ability']:

    def unstable_uniform(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        attaquant = message.source
        if attaquant is None:
            return
        Faces.PlaceCountersOn([attaquant], 1, 'flame', effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Human Torch", card_type=Hero),
            defense=1,
        ),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "You",
            unstable_uniform,
            is_from_attack=True,
        ),
    ]
