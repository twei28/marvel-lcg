from . import *

# Munitions Cache

def GetAbilities() -> Sequence['Ability']:

    def munitions_cache(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        compteurs = [n for n in ('ammo', 'charge') if this.GetCounters(n) > 0]
        if not compteurs or not effect.targets:
            return
        nom = initiator.AskChooseOneText(compteurs)
        Faces.RemoveCountersOn([this], 1, nom, effect)
        Faces.PlaceCountersOn(effect.targets, 1, nom, effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'ammo'),
        AbilityFactory.ThisEnterPlayWithCounters(2, 'charge'),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            munitions_cache
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(
            finder=CardFinder(card_type=Upgrade),
            from_where=["YouControlCards"],
            range=(1, 1),
            another=True
        ),
    ]
