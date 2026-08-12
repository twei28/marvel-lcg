from . import *

# * Carnage — custom « Rainy » (nemesis d'Eddie Brock)
# Quickstrike. Retaliate 1. (portes par cards.json)
# Forced Response: After you heal damage, take 1 damage.

def GetAbilities() -> Sequence['Ability']:

    def sang_pour_sang(effect: 'Effect', message: 'Message.AfterUnitHealHealth') -> None:
        this = effect.this.CastTo(Minion)
        cible = message.trigger
        cible.TakeDamage(this, 1, effect)

    def identite_du_joueur_engage(effect: 'Effect', message: 'Message.AfterUnitHealHealth') -> bool:
        # « you » : le joueur engage avec Carnage ; on vise son identite.
        # Aucune fabrique n'expose le message de soin : Ability construite a
        # la main sur Message.AfterUnitHealHealth, comme The Thing (th001b).
        this = effect.this
        player = this.GetEngagedPlayer()
        return player != None and message.trigger == player.GetIdentity()

    return [
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterUnitHealHealth,
            [
                identite_du_joueur_engage,
            ],
            sang_pour_sang,
        ),
    ]
