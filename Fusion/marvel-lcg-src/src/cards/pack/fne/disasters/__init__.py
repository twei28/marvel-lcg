from cards.pack import *


def CapacitesDeCatastrophe(cout: str, libelle: str, double: Callable[['CardFace'], bool]) -> Sequence['Ability']:
    """Environnement DISASTER : « Uses (2 civilian counters) » = base desc.
    Hero Action: Spend <cout> resources or exhaust a hero or ally you control ->
    remove 1 civilian counter from here (2 counters instead if you exhausted
    <double>).  Deux Hero Actions (RECETTES §5 « or ») : l'une payee en
    ressources, l'autre par CostFunc.Exhaust("Hero|Ally") dont on relit
    `return_exhausted_cards` pour savoir QUI a ete incline."""

    def retirer(effect: 'Effect', n: int) -> None:
        this = effect.this.CastTo(Environment)
        Faces.RemoveCountersOn([this], n, 'civilian', effect)

    def paye(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        retirer(effect, 1)

    inclinaison = CostFunc.Exhaust("Hero|Ally")

    def incline(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        n = 2 if any(double(f) for f in inclinaison.return_exhausted_cards) else 1
        retirer(effect, n)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, paye)
            .SetName(f"Spend {libelle}: remove 1 civilian counter")
            .SetCost(Cost(cout)),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, incline)
            .SetName("Exhaust a hero or ally you control: remove 1 civilian counter (2 instead)")
            .SetCostFunc(inclinaison),
    ]
