from . import *

# * Xavier's Cerebro : AMELIORATION (ITEM. TECH.), cout 5, [mental].
# This card enters play with 2 psy counters on it. Reduce the cost of this card by 1 if you control an upgrade with the TECH trait.
# Hero Action: Remove 1 psy counter from Xavier's Cerebro and exhaust it -> deal 3 damage to each enemy in play.
#
# CARTES DE REFERENCE
#  - `hz006` Heavy Machine Gun : `HeroAction` + `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 1, <pion>)` + `.SetTarget(Enemy, range="All")` + `this.DealDamage(effect.targets, n, effect)`.
#  - `16036` : `ThisEnterPlayWithCounters` (PAS `Uses`) ; `nt005` : reduction conditionnelle.
#
# TEXTE CONTRE CODE
#  « enters play with 2 PSY counters » : 2 pions `psy`. « Remove 1 psy counter AND exhaust it » : DEUX couts. « EACH enemy IN PLAY » : villain + tous les sbires, tous les joueurs. « 3 damage » : 3 a chacun.
#    Pas de limite imprimee : le Cerebro ne sert que 2 fois (2 pions).
#  Chiffres : cout 5, 2 pions, 3 degats.


def GetAbilities() -> Sequence['Ability']:

    def controle_une_amelioration_tech(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and bool(AmeliorationsTech(joueur))

    def cerebro(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.DealDamage(effect.targets, 3, effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[controle_une_amelioration_tech]),
        AbilityFactory.ThisEnterPlayWithCounters(2, 'psy'),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cerebro,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'psy'))
        .SetTarget(Enemy, range="All"),
    ]
