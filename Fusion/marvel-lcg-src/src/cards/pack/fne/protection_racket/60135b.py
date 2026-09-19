from . import *

# Bull in a China Shop 1B — 10, +1 : bases desc.
# Forced Interrupt: When excess damage is dealt to an ally (in expert mode, an
#   ally or a minion) in this play area, place an equal amount of threat on
#   this scheme.
# WhenUnitBeDefeated.excess_damage (sender_unit.py:70) : l'exces n'existe qu'a la defaite.

def GetAbilities() -> Sequence['Ability']:

    def casse(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        exces = int(getattr(message, "excess_damage", 0) or 0)
        if exces > 0:
            this.PlaceThreatOnSchemes([this], exces, effect)

    def concerne(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        unite = message.trigger
        if not DansCetteAire(unite, effect.this):
            return False
        if Ally.IsType(unite):
            return True
        return Minion.IsType(unite) and Worlds.IsExpert(effect)

    return [
        # L'exces n'existe qu'a la defaite : WhenUnitBeDefeated.excess_damage
        # (= -PV restants, sender_unit.py:70) ; AfterUnitTookDamage ne part pas
        # pour le coup fatal (mesure du 18/09/2026).
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedInterrupt, Unit2, casse, conditions=[concerne]),
        *CapacitesCommunes1B(),
    ]
