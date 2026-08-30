from . import *

# Precise Force (1/3) — ATTACK
# Hero Action (attack): Deal up to 3 damage to an enemy.
#
# Modele : determination/dt005.py (Blast Radius) et dt115.py (Whatever it
# Takes), `initiator.DeclareNumber(0, 3)` puis `this.DealDamage(effect.
# targets, value, effect)` -- le joueur declare librement de 0 a 3, sans
# dependre de ce qui a ete effectivement inflige (contrairement a Blast
# Radius qui declare le degat SUBI par le heros).


def GetAbilities() -> Sequence['Ability']:

    def precise_force(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        value = initiator.DeclareNumber(0, 3)
        this.DealDamage(effect.targets, value, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            precise_force,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetName("Precise Force"),
    ]
