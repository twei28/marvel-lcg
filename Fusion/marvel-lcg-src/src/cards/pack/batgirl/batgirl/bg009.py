from . import *

# * James Gordon — soutien, cout 2, [mental]. « Interrupt: When you pay for a card using only [physical] resources, exhaust James
# Gordon → deal 2 damage to an enemy. Interrupt: When you pay for a card using only [energy] resources, exhaust James Gordon →
# draw a card. » Meme fenetre que The Clocktower (bg008) ; deux capacites distinctes, nommees.


def GetAbilities() -> Sequence['Ability']:

    def gordon_degats(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Support)
        this.DealDamage(effect.targets, 2, effect)

    def gordon_pioche(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Interrupt,
            "You",
            None,
            gordon_degats,
            conditions=[lambda e, m: SeulementPaye(m.paid_resources, "R", e)],
        ).SetName("Deal 2 damage").SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Interrupt,
            "You",
            None,
            gordon_pioche,
            conditions=[lambda e, m: SeulementPaye(m.paid_resources, "Y", e)],
        ).SetName("Draw a card").SetCostFunc(CostFunc.Exhaust("This")),
    ]
