from . import *

# The Way of Things — EVENEMENT, cout 1, [mental]. SKILL. THWART. x2 (Iron Fist 7/15).
# Hero Action (thwart): Remove 2 threat from a scheme. You may remove 2 chi counters from Iron
#   Fist to remove 2 threat from a scheme.
#
# CARTES DE REFERENCE
#  - evenement de contre : `luke_cage/62005` « Stand with Me! » / 01012 (`SetLabel('thwart')`,
#    `this.RemoveThreatFromSchemes(cibles, n, effect)`).
#  - « You may remove N counters from <identite> to <effet> » : `venus/__init__.py`
#    `ProposerRetraitDragage` (modele `01165` Eviction Notice) : `MayChooseOneAbility(
#    ForChoiceAbility(...).SetCostFunc(CostFunc.Counter("YourIdentity", n, ...)).SetTarget(...))`.
#
# TEXTE CONTRE CODE
#  ⚠ « You MAY » : branche facultative (bouton Passer), non offerte sous 2 compteurs.
#  ⚠ « from IRON FIST » = l'identite en forme heros (Hero Action).
#  ⚠ « a scheme » ... « a scheme » : DEUX choix independants, la meme manigance est permise
#    (decision utilisateur n°3).
#  ⚠ Le retrait des 2 compteurs est le PRIX de la seconde menace : retires avant elle.


def GetAbilities() -> Sequence['Ability']:

    def way_of_things(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.RemoveThreatFromSchemes([t for t in effect.targets if t is not None], 2, effect)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def seconde(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes([c for c in cibles if c is not None], 2, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Remove 2 chi counters from Iron Fist", seconde)
            .SetCostFunc(CostFunc.Counter("YourIdentity", 2, CHI))
            .SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            way_of_things,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
