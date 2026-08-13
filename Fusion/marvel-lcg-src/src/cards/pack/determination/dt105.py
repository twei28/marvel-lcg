from . import *

# * Venompool

def GetAbilities() -> Sequence['Ability']:

    def bonus_cartes_cachees(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        if player is None:
            return 0
        return min(3, len(player.dealt_encounter_cards.Get()))

    def venompool(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place 2 threat on the main scheme",
                lambda targets: this.PlaceThreatOnSchemes("MainScheme", 2, effect)
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Deal yourself a facedown encounter card",
                lambda targets: initiator.DealEncounterCards(1, effect)
            ).SetHasNoTargetEffect(),
        )

    return [
        *Alias(),
        AbilityFactory.ThisGainKeyword(
            bonus_cartes_cachees,
            attack=1,
            change_on_event=OnEvent.GameArea(),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            venompool
        ),
    ]
