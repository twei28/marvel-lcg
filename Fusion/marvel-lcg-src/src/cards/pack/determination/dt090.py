from . import *

# Psychic Crowd Control

def GetAbilities() -> Sequence['Ability']:

    def psychic_crowd_control(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()

        def confondre_les_sbires(targets: Sequence['CardFace']) -> None:
            sbires = [x for x in Worlds.FindCardsOnField(effect, card_type=Minion,
                                                          engaged_with=initiator)
                      if not x.IsDefeated()]
            if sbires:
                Faces.GiveStatus(sbires, "Confused", effect)

        def frapper_les_confus(targets: Sequence['CardFace']) -> None:
            confus = [x for x in Worlds.FindCardsOnField(effect, card_type=Enemy)
                      if not x.IsDefeated() and x.CastTo(CanStatus).IsConfused()]
            if confus:
                this.DealDamage(confus, 2, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Confuse each minion engaged with you",
                confondre_les_sbires
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Deal 2 damage to each confused enemy",
                frapper_les_confus
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            psychic_crowd_control
        ).SetPlay(only_if_your_identity_has_trait="PSIONIC")
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
