from . import *

# Deck and Cover — custom « DesignHacker »
# Hero Action (attack): Deal 3 damage to an enemy. If that enemy is defeated,
#   change your form.


def GetAbilities() -> Sequence['Ability']:

    def deck_and_cover(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        cible = effect.targets[0]
        this.DealDamage([cible], 3, effect)

        if not cible.IsInPlay() or cible.health <= 0:
            ChoisirEtChangerDeForme(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deck_and_cover,
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
