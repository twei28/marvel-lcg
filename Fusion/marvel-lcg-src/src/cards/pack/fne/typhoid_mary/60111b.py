from . import *

# * Bloody Mary (B) — SCH 1 / ATK 3 / 13[per_hero].
# When Revealed: Deal 1 damage to each identity. (La FAQ du livret : le When
# Revealed de la face qui apparait se resout aussi au retournement.)

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterVillain)
        identites = [j.GetIdentity() for j in effect.world.const_players if j.GetIdentity() is not None]
        if identites:
            this.DealDamage(identites, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeMary("13*"),
    ]
