from . import *

# * War Witches — custom "Rainy" (némésis de Thor Jane Foster)
# [star] Forced Interrupt: When War Witches would attack, they scheme instead.
# Forced Response: After threat is placed on the main scheme, the engaged
# player takes 1 indirect damage.

def GetAbilities() -> Sequence['Ability']:

    def GetEngagedPlayer(effect: 'Effect', this: 'Minion') -> 'Player|None':
        for player in list(effect.world.players):
            if player.is_eliminated:
                continue
            if this in player.GetEngagedMinions():
                return player
        return None

    def scheme_instead(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        player = message.property.against_player or GetEngagedPlayer(effect, this)
        if player:
            this.DoSchemes(player, effect)

    def after_threat_on_main(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        this = effect.this.CastTo(Minion)
        player = GetEngagedPlayer(effect, this)
        if player:
            player.GetIdentity().TakeIndirectDamage(this, 1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            scheme_instead,
        ),
        AbilityFactory.AfterSchemePlaceThreat(
            AbilityType.ForcedResponse,
            MainScheme,
            after_threat_on_main,
        )
    ]
