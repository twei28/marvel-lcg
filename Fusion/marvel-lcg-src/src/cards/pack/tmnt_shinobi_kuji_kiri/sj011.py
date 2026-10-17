from . import *

# Unravel (sj011), Kuji-Kiri, evenement ATTACK SPELL THWART (Inkwire, TMNT Shinobi).
# Hero Action (attack/thwart): Discard 3 cards from the top of your deck and discard 3 cards from the top of the
# encounter deck → deal 3 damage to an enemy and remove 3 threat from a scheme.
#
# Cartes de reference : `gam/18020` Hit and Run (« Deal N damage to an enemy. Remove N threat from a scheme » :
# `SetTarget(Enemy)` + `SetTarget2(Scheme2)`, label 'attack','thwart') ; couts de defausse de deck :
# `CostFunc.DiscardDeckTopCards("YourDeck", N)` (Rampage, arbitrage du 25/09/2026 : deck court -> deck epuise,
# cout paye) et `("EncounterDeck", N)` (`falcon/53010`).
#
# TEXTE CONTRE CODE
#  ⚠ « → » : les DEUX defausses (3 du deck joueur ET 3 du deck rencontre) sont le COUT, payees avant les
#    effets ; « deal 3 damage to AN enemy AND remove 3 threat from A scheme » : deux cibles distinctes
#    (ennemi, manigance), les deux effets se resolvent.
#  ⚠ Labels 'attack' et 'thwart' (parenthese imprimee).


def GetAbilities() -> Sequence['Ability']:

    def unravel(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 3, effect)
        this.RemoveThreatFromSchemes(effect.targets2, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            unravel,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 3))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("EncounterDeck", 3))
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]
