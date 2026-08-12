from . import *

# * Donald Pierce — custom « Kajislav »
# Resource: Exhaust Donald Pierce -> generate a [wild] resource.
# Response: After you resolve Albert's "Initiate Protocol" ability, ready
# this card.

def GetAbilities() -> Sequence['Ability']:

    def ready_pierce(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Support)
        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenResolveSpecialAbility(
            CardFinder(name="Albert", card_type=Hero),
            ready_pierce,
        ),
    ]
