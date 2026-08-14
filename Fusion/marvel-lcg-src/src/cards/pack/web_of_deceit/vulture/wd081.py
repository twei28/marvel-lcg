from . import *

# Vulturion

def GetAbilities() -> Sequence['Ability']:

    def defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # « When Defeated: Discard 1 card at random from the engaged player's
        # hand. »
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        if joueur:
            joueur.DiscardRandomHandCards(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Discard 1 card at random from your hand. »
        message.GetToPlayer().DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
