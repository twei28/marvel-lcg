from . import *

# Battle in the Bodega 1B — 10 menaces, +1 : bases desc.
# Forced Response: After a character in this play area is attacked, deal 1
#   damage to the attacker and place 1 threat here. (Limit once per phase in
#   standard mode.)
# If any main scheme is completed or any player is eliminated, the players
#   lose the game.  (CapacitesCommunes1B)
# « in this play area » = DansCetteAire ; la limite ne vaut qu'en mode normal
# (deux capacites, l'une limitee et l'autre non, selon Worlds.IsExpert).

def GetAbilities() -> Sequence['Ability']:

    def riposte(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(MainScheme)
        attaquant = message.attacker
        if attaquant is not None and attaquant.IsInPlay():
            this.DealDamage([attaquant], 1, effect)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def dans_cette_aire(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        return DansCetteAire(message.attacked, effect.this)

    normal = AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, Enemy, "YouControlCharacter", riposte,
                                               conditions=[dans_cette_aire, lambda e, m: not Worlds.IsExpert(e)]).LimitOncePerPhase()
    expert = AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, Enemy, "YouControlCharacter", riposte,
                                               conditions=[dans_cette_aire, lambda e, m: Worlds.IsExpert(e)])
    return [normal, expert, *CapacitesCommunes1B()]
