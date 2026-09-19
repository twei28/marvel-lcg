from . import *

# Hung Out to Dry 1B — 10, +1 : bases desc.
# Forced Response: After a character enters play in this play area, deal 1
#   damage to it and place 1 threat here.
# AfterCardEnterPlay(Character) filtre par DansCetteAire (sbire engage avec le
# proprietaire compris).

def GetAbilities() -> Sequence['Ability']:

    def serre(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(MainScheme)
        unite = message.trigger
        if unite.IsInPlay():
            this.DealDamage([unite], 1, effect)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def concerne(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        unite = message.trigger
        return Unit2.IsType(unite) and DansCetteAire(unite, effect.this)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, None, serre, conditions=[concerne]),
        *CapacitesCommunes1B(),
    ]
