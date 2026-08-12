from . import *

# * Peter Parker — custom « Rainy »
# Uncle Ben's Wisdom — Action: Discard 1 card from your hand -> search your
#   deck and discard pile for a Great Power or Great Responsibility resource
#   and add it to your hand. Shuffle your deck. (Limit twice per round.)
# (Impact Webbing sr012, carte de regles Permanent/Setup, sort au setup :
#  meme montage que « The Trunk » ah012a chez Totally Awesome Hulk.)

def GetAbilities() -> Sequence['Ability']:

    def uncle_bens_wisdom(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_ids=["sr007", "sr008"],
            card_type=Resource,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.SetupPutIntoPlay(
            ["sr012"],
        ),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            uncle_bens_wisdom,
            conditions=[LimiteDeuxParRound],
        ).SetName("Uncle Ben's Wisdom")
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
