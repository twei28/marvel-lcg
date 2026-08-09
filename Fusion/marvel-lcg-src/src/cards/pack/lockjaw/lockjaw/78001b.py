from . import *

# * Lockjaw (face alter-ego) — custom « Nugget »
# Setup: Search your deck, hand and discard pile for Tuning Fork and put it
#   into play.
# Cheer Up — Response: After you change to this form, ready a friendly
#   character.


def GetAbilities() -> Sequence['Ability']:

    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        initiator = effect.GetInitiator()

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            include_player_hand_cards=True,
            name="Tuning Fork",
            card_type=Upgrade,
        )
        if face:
            face.PutIntoPlay(initiator, effect)

    def cheer_up(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            setup
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            cheer_up,
            to_this_form=True,
        ).SetName("Cheer Up")
        .SetTarget(Friend, canbe_ready=True),
    ]
