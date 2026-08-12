from . import *

# * Gwendolyn Poole — custom « ekAugust »
# "I Won't Be an Extra" — Action: Find a Gwenpool card and add it to your
# hand. (Limit once per phase.)

def GetAbilities() -> Sequence['Ability']:

    def i_wont_be_an_extra(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            set_name="Gwenpool",
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            i_wont_be_an_extra
        ).SetName("I Won't Be an Extra")
        .LimitOncePerPhase(),
    ]
