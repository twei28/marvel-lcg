from . import *

# Prodigy (David Alleyne), allie CAPTIVE MUTANT. « Response : After you play Prodigy from hand, draw 1 card. »
# Carte de reference : sj012 (`AfterPlayerPlayedCard(Response, "You", "This", op, from_hand=True)`, recette « After you play X from your hand » sur la
# carte elle-meme), `player.DrawUp`.


def GetAbilities() -> Sequence['Ability']:
    def pioche(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        message.to_player.DrawUp(1, effect)

    return [AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, "You", "This", pioche, from_hand=True), CaptifRecrute()]
