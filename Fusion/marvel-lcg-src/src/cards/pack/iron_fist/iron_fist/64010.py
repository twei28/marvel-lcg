from . import *

# Feel the Flow — AMELIORATION, cout 0, [mental]. TECHNIQUE. x1 (Iron Fist 13/15).
# Temporary.
# Hero Action (thwart): Remove 1 chi counter from Iron Fist -> remove 1 threat from a scheme.
#
# CARTES DE REFERENCE
#  - Hero Action (thwart) a cible sur une carte en jeu : `michelangelo/tm009` et `fne/60027`
#    (`RemoveThreatFromSchemes`, l'amelioration passe la main a l'identite, upgrade.py) ;
#  - cout en compteurs pris sur l'identite : `venus/tv001b` (`CostFunc.Counter("YourIdentity", ...)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Remove 1 chi counter from Iron Fist -> » : COUT (fleche), sur l'identite ; non offert sans chi.
#  ⚠ « (thwart) » : `SetLabel('thwart')`.
#  ⚠ « a scheme » : n'importe quelle manigance.
#  ⚠ Temporary : base automatique ; perdu tant que Danny Rand est face visible (64001b).


def GetAbilities() -> Sequence['Ability']:

    def sentir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.RemoveThreatFromSchemes([t for t in effect.targets if t is not None], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sentir,
            conditions=[AuMoinsChi(1)],
        ).SetLabel('thwart')
        .SetTarget(Scheme2)
        .SetCostFunc(CostFunc.Counter("YourIdentity", 1, CHI)),
    ]
