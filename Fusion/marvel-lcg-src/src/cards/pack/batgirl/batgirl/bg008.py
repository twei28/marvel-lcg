from . import *

# * The Clocktower — soutien, cout 1, [wild]. « Alter-Ego Action: Exhaust this card → draw 1 card and remove 1 threat from a scheme.
# Hero Interrupt: When you pay for a card using only [mental] resources, exhaust this card → remove up to 2 threat from a scheme. »
# Cartes de reference : `01026` Superhuman Law Division (action d'alter ego, `RemoveThreatFromSchemes`), `norman` ho006
# (`WhenPlayerPlayCard(HeroInterrupt, "You", ...)` : la fenetre « when you pay for / play a card », `message.paid_resources`).


def GetAbilities() -> Sequence['Ability']:

    def clocktower_ae(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    def clocktower_hero(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Support)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    def paye_mental(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        return SeulementPaye(message.paid_resources, "B", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            clocktower_ae,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.HeroInterrupt,
            "You",
            None,
            clocktower_hero,
            conditions=[paye_mental],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
    ]
