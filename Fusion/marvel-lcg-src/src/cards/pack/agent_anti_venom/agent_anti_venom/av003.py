from . import *

# Dig Deep — custom « DesignHacker »
# Hero Action (attack): Deal 3 damage to an enemy. If Agent Anti-Venom has
#   exactly 10 hit points remaining, remove 1 threat from a scheme and stun
#   that enemy.

def GetAbilities() -> Sequence['Ability']:

    def dig_deep(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        # La condition se lit AVANT de frapper : les degats infliges a un
        # ennemi ne changent pas les PV du heros, mais un Retaliate, si.
        intact = HasExactlyTen(effect)

        this.DealDamage(effect.targets, 3, effect)

        if intact:
            Faces.GiveStatus(effect.targets, "Stunned", effect)
            initiator = effect.GetInitiator()
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 threat from a scheme",
                    lambda targets:
                        this.RemoveThreatFromSchemes(targets, 1, effect)
                ).SetTarget(Scheme2)
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dig_deep,
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
