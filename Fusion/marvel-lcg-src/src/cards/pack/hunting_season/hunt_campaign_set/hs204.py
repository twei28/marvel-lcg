from . import *

# hs204 * Vermin (sbire, ajoute au deck rencontre de Kraven si Vermin s'est echappe)
# Entre en jeu avec 3 pions rat. Forced Interrupt : quand il subirait des degats,
# retire un pion rat a la place.

def GetAbilities() -> Sequence['Ability']:

    def a_des_rats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return effect.this.GetCounters('rat') > 0

    def esquiver(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.SetBeInstead(effect)
        Faces.RemoveCountersOn([effect.this], 1, 'rat', effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(3, 'rat'),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", esquiver, conditions=[a_des_rats]),
    ]
