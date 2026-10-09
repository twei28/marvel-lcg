from . import *

# Lizard Thrall

def GetAbilities() -> Sequence['Ability']:

    def attaque_a_la_place(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        ETAT["en_cours"] = True
        try:
            message.SetBeInstead(effect)
            effect.this.CastTo(Enemy).DoAttackYou(message.GetAgainstPlayer(), effect)
        finally:
            ETAT["en_cours"] = False

    def manigance_a_la_place(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        ETAT["en_cours"] = True
        try:
            message.SetBeInstead(effect)
            effect.this.CastTo(Enemy).DoSchemes(message.GetAgainstPlayer(), effect)
        finally:
            ETAT["en_cours"] = False

    libre = lambda effect, message: not ETAT["en_cours"]

    return [
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", attaque_a_la_place, conditions=[libre]),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", manigance_a_la_place, conditions=[libre]),
    ]
