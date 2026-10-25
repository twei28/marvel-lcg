from . import *

# Gamma Slam (variante Why Not) : cout 3 au lieu de 4, trait GAMMA ajoute
# (desc et traits, cards.json). Texte inchange : modele 01021.


def GetAbilities() -> Sequence['Ability']:

    def gamma_slam(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        value = min(15, initiator.GetIdentity().sustained)
        this.DealDamage(effect.targets, value, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            gamma_slam
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
