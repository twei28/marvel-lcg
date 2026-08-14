from . import *

# Quick Reload

def GetAbilities() -> Sequence['Ability']:

    def recharger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action: Choose two of the following (you may choose the same
        # option twice):
        #   • Ready a TECH card you control.
        #   • Place 1 all-purpose counter on a TECH upgrade you control. »
        joueur = effect.GetInitiator()

        for _ in range(2):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready a TECH card you control",
                    lambda cibles: Faces.ReadyAll(cibles, effect)
                ).SetTarget(CardFinder(trait="TECH", canbe_ready=True)),
                AbilityFactory.ForChoiceAbility(
                    "Place 1 all-purpose counter on a TECH upgrade you control",
                    lambda cibles: Faces.PlaceCountersOn(cibles, 1, "all-purpose", effect)
                ).SetTarget(CardFinder(trait="TECH", card_type=Upgrade)),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            recharger
        ).SetPlay(),
    ]
