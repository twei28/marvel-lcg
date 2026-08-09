from . import *

# Yancy Street Gang — custom « DesignHacker »
# Action: Exhaust Yancy Street Gang -> deal 1 damage to a character. This
# damage gains piercing. If a tough status card was discarded this way, ready
# Yancy Street Gang.

def GetAbilities() -> Sequence['Ability']:

    def yancy_street_gang(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)

        avant = [x for x in effect.targets if x.CastTo(Unit2).IsTough()]

        this.DealDamage(effect.targets, 1, effect,
                        property=AttackProperty(piercing=True))

        # Le perçant défausse le tough avant les dégâts : si une cible en
        # avait un et ne l'a plus, il a bien été défaussé par cette attaque.
        for cible in avant:
            if not cible.CastTo(Unit2).IsTough():
                Faces.ReadyAll([this], effect)
                break

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            yancy_street_gang
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Unit2),
    ]
