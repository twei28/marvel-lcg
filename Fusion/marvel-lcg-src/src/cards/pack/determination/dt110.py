from . import *

# Temporal Bubble

def GetAbilities() -> Sequence['Ability']:

    def temporal_bubble(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        x = initiator.DeclareNumber(0, len(initiator.hand_cards.Get()))
        if x <= 0:
            return

        def defausser_et_encaisser(targets: Sequence['CardFace']) -> None:
            initiator.DiscardHandCards((x, x), effect)
            initiator.GetHero().TakeDamage(this, x, effect)

        def prendre_des_rencontres(targets: Sequence['CardFace']) -> None:
            initiator.DealEncounterCards(x, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard X cards from your hand and take X damage",
                defausser_et_encaisser
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Deal yourself X facedown encounter cards",
                prendre_des_rencontres
            ).SetHasNoTargetEffect(),
        )

        for _ in range(x):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready a card you control",
                    lambda targets: Faces.ReadyAll(targets, effect)
                ).SetTarget("YouControlCards", canbe_ready=True)
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            temporal_bubble
        ).SetPlay(),
    ]
