from . import *

# Dog Catcher — custom « Nugget » (némésis de Lockjaw)
# Surge. (clé desc, gérée nativement)
# [star] Forced Interrupt: When Dog Catcher would scheme, it attacks instead.


def GetAbilities() -> Sequence['Ability']:

    def attaque_au_lieu_de_comploter(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Minion)

        joueur = this.GetEngagedPlayer()
        if joueur is None:
            joueur = message.GetToPlayer() if hasattr(message, "GetToPlayer") else None
        if joueur is None:
            return

        message.SetBeInstead(effect)
        this.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "This",
            attaque_au_lieu_de_comploter,
        ),
    ]
