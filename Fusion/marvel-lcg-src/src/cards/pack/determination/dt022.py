from . import *

# * Cloak

def GetAbilities() -> Sequence['Ability']:

    def cloak(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        for face in effect.targets:
            # « attach it to him facedown » : c'est le tuck du moteur, qui pose
            # la carte face cachee sous celle-ci (60030 Contingency Planning).
            this.TuckCardUnderHere(face, effect)

    return [
        *AbilityFactory.AttachedCardCanPlayLikeInHand(
            CardFinder(card_type=Ally|Upgrade)
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cloak
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(
            finder=CardFinder(card_type=Ally|Upgrade),
            from_where=['YourHandCards'],
            range=(1, 1)
        ),
    ]
