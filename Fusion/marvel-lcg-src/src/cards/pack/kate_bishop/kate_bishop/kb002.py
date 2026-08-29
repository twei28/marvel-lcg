from . import *

# * Hawkeye: Clint Barton
# Interrupt: When Hawkeye would be defeated by consequential damage, shuffle
#   him into your deck and place 1 arrow counter on Kate's Bow.
#
# Modele : Deadpool (next_evol/40024.py), meme structure
# `WhenUnitWouldBeDefeated(..., by_consequential_damage=True)` +
# `message.SetBeInstead(effect)`. « Shuffle him into your deck » : James
# Rhodes (warm/war_machine/23001b.py), `Faces.ShuffleAllTo(targets,
# player.player_deck, effect)`.


def GetAbilities() -> Sequence['Ability']:

    def hawkeye(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Ally)

        message.SetBeInstead(effect)

        player = this.GetControlByPlayer()
        if player:
            Faces.ShuffleAllTo([this], player.player_deck, effect)

        PlacerCompteursFlecheSurArc(effect, 1)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "This",
            hawkeye,
            by_consequential_damage=True,
        ),
    ]
