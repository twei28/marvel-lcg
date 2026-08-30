from . import *

# * Harvester — sbire ASSASSIN.
# Quickstrike.
# Harvester's attacks gain piercing.
# Forced Response: After Harvester attacks and damages a character, deal 1
#   damage to that character.
#
# Quickstrike : mot-cle purement declaratif (`desc.Quickstrike`, deja dans
# cards.json), aucun code. "Harvester's attacks gain piercing" : modele
# officiel exact 04027 Crossfire, `AbilityFactory.UnitAttackGainKeyword
# ("This", piercing=True)`. "After Harvester attacks and damages a
# character, deal 1 damage to that character" : modele core/klaw/01118.py
# (Sonic Converter), `AbilityFactory.AfterUnitAttackAndDamageUnit
# (ForcedResponse, "This", "Character", ...)` + `message.attacked`.


def GetAbilities() -> Sequence['Ability']:

    def harvester_response(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)

        this.DealDamage([message.attacked], 1, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            harvester_response,
            target_in_play=True,
        ),
    ]
