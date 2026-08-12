from . import *

# Symbiote Rioter — custom « Rainy » (nemesis d'Eddie Brock)
# Guard. Patrol. (portes par cards.json)
# Forced Response: After you attack another enemy, take 1 damage.

def GetAbilities() -> Sequence['Ability']:

    def represailles(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        player = this.GetEngagedPlayer()
        if player:
            player.GetIdentity().TakeDamage(this, 1, effect)

    def mon_joueur_attaque_un_autre(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        this = effect.this
        player = this.GetEngagedPlayer()
        if player == None:
            return False
        if message.attacker != player.GetIdentity():
            return False
        return this not in message.attacked_targets

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            Identity,
            Enemy,
            represailles,
            conditions=[mon_joueur_attaque_un_autre],
        ),
    ]
