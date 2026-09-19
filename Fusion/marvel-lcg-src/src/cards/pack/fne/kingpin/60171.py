from . import *

# * Spot (CRIMINAL UNDERLING) — SCH 2 / ATK 2 / 5 PV, boost 3.
# Enters play with 1 spot counter on him.
# Forced Interrupt: When Spot would be dealt damage from an attack, if there is
#   at least 1 spot counter here, remove 1 spot counter from here and deal that
#   damage to the attacker instead. Otherwise, place 1 spot counter here.
# Modeles : sr015 Mysterio (ThisEnterPlayWithCounters + WhenUnitWouldTakeDamage
# "This" + PreventDamage("All")), l'attaquant = message.would_atk_message.attacker.

def GetAbilities() -> Sequence['Ability']:

    def portail(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Minion)
        if this.GetCounters('spot') >= 1:
            total = message.will_take_damage
            message.PreventDamage("All", effect)
            Faces.RemoveCountersOn([this], 1, 'spot', effect)
            attaque = message.would_atk_message
            attaquant = attaque.attacker if attaque is not None else None
            if attaquant is not None and total > 0:
                this.DealDamage([attaquant], total, effect)
        else:
            Faces.PlaceCountersOn([this], 1, 'spot', effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(1, 'spot'),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", portail, is_from_attack=True),
    ]
