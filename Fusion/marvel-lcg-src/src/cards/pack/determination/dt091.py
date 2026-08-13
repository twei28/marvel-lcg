from . import *

# Determined Energy

def GetAbilities() -> Sequence['Ability']:

    def determined_energy(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)

        initiator = effect.GetInitiator()

        def donner(nom: str, finder: 'CardFinder') -> None:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Give %s a tough status card" % nom,
                    lambda targets: Faces.GiveStatus(targets, "Tough", effect)
                ).SetTarget(finder)
            )

        donner("an ally", CardFinder(card_type=Ally))
        donner("a minion", CardFinder(card_type=Minion))

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroInterrupt,
            determined_energy,
            to_pay_card=CardFinder2("TACTIC"),
        ),
    ]
