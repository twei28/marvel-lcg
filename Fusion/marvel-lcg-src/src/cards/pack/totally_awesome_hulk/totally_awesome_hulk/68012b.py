from . import *

# "The Trunk" — face B — custom « DesignHacker »
# Permanent.
# Forced Response: After Uncontrollable Hulk attacks, remove a rage counter
#   from this card.
# Forced Interrupt: When there are no rage counters here, flip this card and
#   change form to Amadeus Cho.


def GetAbilities() -> Sequence['Ability']:

    def calm_down(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Support)

        Faces.RemoveCountersOn([this], 1, 'rage', effect)

    def back_to_cho(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        this = effect.this.CastTo(Support)
        player = this.GetControlByPlayer()

        this.card.Flip(effect)
        if player is not None:
            player.GetIdentity().ChangeToForm(AlterEgo, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="Uncontrollable Hulk"),
            calm_down,
        ),
        AbilityFactory.IfThereIsNoCounterHere(
            'rage',
            back_to_cho,
        ),
    ]
