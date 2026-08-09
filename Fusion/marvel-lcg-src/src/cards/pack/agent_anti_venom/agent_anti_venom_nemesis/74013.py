from . import *

# * Maniac — custom « DesignHacker » (sbire nemesis d'Agent Anti-Venom)
# Forced Response: After Maniac attacks an ally you control, deal X damage to
#   your hero, where X is that ally's printed ATK.

def GetAbilities() -> Sequence['Ability']:

    def maniac(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)

        cible = message.attacked
        if cible is None or not Ally.IsType(cible):
            return

        player = cible.CastTo(Ally).GetControlByPlayer()
        if player is None:
            return

        hero = player.GetHero()
        if hero is None:
            return

        value = cible.printed_attack
        if value > 0:
            this.DealDamage([hero], value, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            Ally,
            maniac,
        ),
    ]
