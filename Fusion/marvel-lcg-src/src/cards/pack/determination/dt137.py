from . import *

# Calculated Action

def GetAbilities() -> Sequence['Ability']:

    def calculated_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        # X + Y = 6 : le joueur declare X, Y suit.
        x = initiator.DeclareNumber(0, 6)

        ennemi = None
        for cible in effect.targets:
            if Enemy.IsType(cible):
                ennemi = cible
            elif Scheme2.IsType(cible):
                this.RemoveThreatFromSchemes([cible], 6 - x, effect)
        if ennemi is not None and x > 0:
            avant = ennemi.CastTo(CanHealth).health
            this.DealDamage([ennemi], x, effect)
            if ennemi.CastTo(Unit2).IsDefeated() and avant == x:
                Faces.ReadyAll([initiator.GetHero()], effect)
                return
        initiator.GetHero().TakeDamage(this, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            calculated_action
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget("Enemy|Scheme", range=(1, 2)),
    ]
