from . import *

# Counterstrike

def GetAbilities() -> Sequence['Ability']:

    # « une attaque avec overkill vainc un allie que vous controlez ET vous
    # blesse » : le moteur ne publie pas le drapeau overkill sur ce message,
    # mais il publie ce que l'overkill PRODUIT — l'identite du controleur
    # figure parmi les cibles touchees par l'attaque, ce qui n'arrive que par
    # le debordement (can_attack.py:350-407). C'est la meme chose, lue par son
    # effet plutot que par son nom.
    def check_defeated_and_you_damaged(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        if player is None:
            return False
        if not message.has_defeated_target:
            return False
        return player.GetIdentity() in message.took_damage_targets

    def counterstrike(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        ally = message.attacked.CastTo(Unit2)
        value = ally.attack + player.GetHero().attack
        this.DealDamage(effect.targets, value, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.HeroResponse,
            None,
            "YouControlCharacter",
            counterstrike,
            conditions=[check_defeated_and_you_damaged],
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Enemy),
    ]
