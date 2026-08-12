from . import *

# Totally Awesome — custom « Rainy »
# Hero Response: After you play a card from your reserve, remove 1 threat from
#   a scheme.

def GetAbilities() -> Sequence['Ability']:

    def retirer_une_menace(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)

        if effect.targets:
            this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        ApresCarteJoueeDepuisLaReserve(
            AbilityType.HeroResponse,
            retirer_une_menace,
            hero_form_only=True,
        ).SetTarget(Scheme2, range=(1, 1)),
    ]
