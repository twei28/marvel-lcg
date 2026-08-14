from . import *

# * Typhoid Mary

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Take 1 indirect damage for each pursuit counter on
        # Pursued by the Past. »
        this = effect.this.CastTo(Minion)
        combien = NombreDeCompteursDePoursuite(effect)
        if combien > 0:
            message.GetToPlayer().GetIdentity().TakeIndirectDamage(this, combien, effect)

    return [
        # « [star] Typhoid Mary's attacks deal indirect damage. »
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            indirect_damage=True,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
