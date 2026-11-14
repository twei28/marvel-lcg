from . import *

# Astral Projection (x2) : EVENEMENT (THWART. PSIONIC.), cout 2, [mental]. Classe Hero.
# Hero Action (thwart): Remove 3 threat from a scheme. Remove 1 additional threat for each icon ([star] and [boost]) on the card tucked under Glimpse of the Future.
#
# CARTES DE REFERENCE
#  - `01060` (core) : evenement a etiquette thwart, `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('thwart')`.
#  - `mt` `RetirerUneMenace` : `RemoveThreatFromSchemes(cibles, n, effect)` avec `SetTarget(Scheme2)`.
#
# TEXTE CONTRE CODE
#  « a scheme » : principale ou annexe, au choix. « 3 threat ... 1 ADDITIONAL for EACH icon » : 3 + X, X lu a la resolution. Retrait direct, pas un contre de base.
#  Chiffres : cout 2, 3 menace + X.


def GetAbilities() -> Sequence['Ability']:

    def astral_projection(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 3 + IconesSousGlimpse(joueur), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            astral_projection,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
