from . import *

# * Thor (Jane Foster) — custom "Rainy"
# Worthy — Action: Search your deck and discard pile for the Mjolnir upgrade
# and add it to your hand. Shuffle your deck. (Limit once per round.)

def GetAbilities() -> Sequence['Ability']:

    def worthy(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        initiator = effect.GetInitiator()

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_ids=["ra007"],
            card_type=Upgrade,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            worthy
        ).SetName("Worthy")
        .LimitOncePerRound()
    ]
