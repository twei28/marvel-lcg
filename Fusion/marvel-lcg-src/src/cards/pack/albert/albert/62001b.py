from . import *

# * Albert (alter-ego) — custom « Kajislav »
# Extensive Development — Setup: Search your deck and discard pile for an
# ENHANCEMENT upgrade and put it into play.

def GetAbilities() -> Sequence['Ability']:

    def extensive_development(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this
        initiator = effect.GetInitiator()

        def action():
            face = Search.PlayerCard(
                effect,
                initiator,
                include_player_deck=True,
                include_discard_pile=True,
                trait="ENHANCEMENT",
                card_type=Upgrade,
            )
            if face:
                face.PutIntoPlay(initiator, effect)

        RunAt.WhenCardSetup(this, action)

    return [
        AbilityFactory.WhenPlayerSelectHero(
            "This",
            extensive_development,
        ).SetName("Extensive Development")
    ]
