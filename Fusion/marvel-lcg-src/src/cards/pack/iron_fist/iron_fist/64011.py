from . import *

# Keep 'Em Coming — AMELIORATION, cout 0, [physical]. TECHNIQUE. x1 (Iron Fist 14/15).
# Temporary.
# Hero Action: Remove 2 chi counters from Iron Fist -> ready him.
#
# CARTES DE REFERENCE
#  - redresser : `Faces.ReadyAll(faces, effect)` (RECETTES §2, an001a, ho011).
#  - cout en compteurs pris sur l'identite : `venus/tv001b`.
#
# TEXTE CONTRE CODE
#  ⚠ « Remove 2 chi counters from Iron Fist -> » : COUT de 2 ; non offert sous 2 compteurs.
#  ⚠ « ready HIM » = Iron Fist, l'identite (forme heros : Hero Action).
#  ⚠ Temporary : base automatique ; perdu tant que Danny Rand est face visible (64001b).


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        identite = IdentiteDuJoueur(effect)
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            redresser,
            conditions=[AuMoinsChi(2)],
        ).SetCostFunc(CostFunc.Counter("YourIdentity", 2, CHI)),
    ]
