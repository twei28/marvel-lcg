from . import *

# * Totally Awesome Hulk — custom « DesignHacker »
# Losing Control — You can only change to BRUTE hero form by resolving the
#   effects of "The Trunk" support.
# Hypermind — Treat all resources you generate as [wild] resources.


def GetAbilities() -> Sequence['Ability']:

    def hypermind(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> None:
        # Toute source de ressources contrôlée par ce joueur produit du [wild].
        res = message.res
        if res.val <= 0:
            return
        message.SetResources(Resources("G") * res.val, effect)

    def is_your_payment(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> bool:
        return message.GetToPlayer() == effect.this.GetControlByPlayer()

    return [
        LosingControlGuard(),
        Ability(
            AbilityType.NonKeyword,
            Message.CheckEffectGeneratedResources,
            [is_your_payment],
            hypermind,
        ).SetName("Hypermind"),
    ]
