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
            # CORRECTIF 20/10/2026 (backlog 13, trouve par l'autoplay du deck
            # de test) : `OnEvent.GameArea()` n'a pas de `GenerateAbilities`
            # (on_event.py : `assert False`) et faisait planter l'entree en jeu
            # de Venompool ; le bonus d'ATQ ne partait jamais. La valeur suit
            # les cartes distribuees face cachee : meme evenement que 17010
            # Star-Lord's Helmet.
            change_on_event=OnEvent.DealtEncounterCard("You"),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            venompool
        ),
    ]
