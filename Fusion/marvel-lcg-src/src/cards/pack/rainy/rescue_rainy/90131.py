from . import *

# Innocent Bystander

def GetAbilities() -> Sequence['Ability']:

    def liberer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)

        this.RemoveThreatFromSchemes(effect.targets, 1, effect)
        Faces.DiscardAll([this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            hand_size=-1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            liberer
        ).SetCostFunc(CostFunc.Exhaust("YourHero"))
        .SetTarget(Scheme2),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
