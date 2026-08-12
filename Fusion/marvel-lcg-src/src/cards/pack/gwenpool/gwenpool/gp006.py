from . import *

# Endless Storylines — custom « ekAugust »
# Hero Response: After you spend this card, ____ and ____.
# Bulles : « Remove 1 threat from a scheme. » / « Heal 1 damage from
# Gwenpool. » / « Deal 1 damage to an enemy. »

def GetAbilities() -> Sequence['Ability']:

    def endless_storylines(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)

        ResolveBlank(effect, 2)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            endless_storylines,
        ),
    ]
