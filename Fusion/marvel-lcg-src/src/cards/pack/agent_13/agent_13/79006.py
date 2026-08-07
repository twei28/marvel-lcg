from . import *

# Takedown — custom « Rainy »
# Hero Response (attack): After you attack an enemy, deal 2 damage to an
# enemy. If that enemy is defeated by this attack, draw 1 card.
#
# Modele pour le declencheur : Pitchback (28012, Nova), meme structure
# « Hero Response, apres que ton heros attaque -> inflige X degats a un
# ennemi » via AfterUnitAttackEnd / "YourHero".
# Modele pour le tirage conditionne : Sock 'Em (67009, The Thing), qui passe
# `if_this_attack_defeats` a DealDamage pour ne resoudre l'effet que si CETTE
# attaque-la vainc la cible.

def GetAbilities() -> Sequence['Ability']:

    def takedown(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        def vaincu(unit: 'Unit2') -> None:
            Unused(unit)
            initiator.DrawUp(1, effect)

        this.DealDamage(effect.targets, 2, effect, if_this_attack_defeats=vaincu)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.HeroResponse,
            "YourHero",
            takedown
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
