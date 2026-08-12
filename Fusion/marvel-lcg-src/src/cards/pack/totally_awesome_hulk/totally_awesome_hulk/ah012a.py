from . import *

# "The Trunk" — face A — custom « DesignHacker »
# Permanent. Setup.
# Forced Response: After Totally Awesome Hulk takes any amount of damage, add a
#   rage counter here.
# Forced Interrupt: When there are 4 rage counters here, flip this card and
#   change form to Uncontrollable Hulk.


def GetAbilities() -> Sequence['Ability']:

    def rage(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Support)

        Faces.PlaceCountersOn([this], 1, 'rage', effect)

    def hulk_out(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Support)
        player = this.GetControlByPlayer()

        this.card.Flip(effect)
        if player is not None:
            ChangeToBruteForm(player, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.ForcedResponse,
            CardFinder(name="Totally Awesome Hulk"),
            rage,
        ),
        AbilityFactory.IfThereAreAtLeastCounterHere(
            4,
            'rage',
            hulk_out,
        ),
    ]
