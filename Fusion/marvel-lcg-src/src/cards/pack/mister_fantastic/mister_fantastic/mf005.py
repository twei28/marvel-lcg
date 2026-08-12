from . import *

# Fantasticar — custom « DesignHacker »
# Mister Fantastic gets +1 hand size.
# Hero Action: Exhaust Fantasticar -> choose a player in hero form. Reduce the
# cost of the next event card that player plays this phase by 1.

def GetAbilities() -> Sequence['Ability']:

    def fantasticar(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        for target in effect.targets:
            player = target.GetControlByPlayer()
            if player is None or not player.IsHero():
                continue
            Worlds.UpdateNextCardPlayCost(
                player,
                -1,
                effect,
                finder=CardFinder(card_type=Event),
                in_this="Phase",
            )

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Mister Fantastic", card_type=Hero),
            hand_size=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fantasticar
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("Players"),
    ]
