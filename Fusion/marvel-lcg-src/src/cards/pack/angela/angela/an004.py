from . import *

# Murderous Glare — evenement. THWART. Cout 0. x3
# Response (thwart): After Angela attacks and defeats an enemy, remove 2
#   threat from a scheme. Remove 1 additional threat from that scheme for
#   each minion you defeated this round.
#
# Cartes de reference : vp001a Fear Factor (pack venompool) pour
# `AfterUnitDefeatedUnit` + `RemoveThreatFromSchemes(effect.targets, n, effect)`
# avec `SetTarget(Scheme2, range=(1, 1))`.
#
# ⚠ TROIS mots-pieges sur cette seule carte (PROCESSUS-CARTE etape 5) :
#  - « attacks AND defeats » : le declencheur exige que la defaite vienne
#    d'une ATTAQUE, d'ou `is_from_attack=True`. Une carte qui tue par des
#    degats directs ne doit rien declencher.
#  - « defeats an ENEMY », pas « a minion » : le vilain compte. Contraste
#    voulu avec an001a Frenzy et an009 Xiphos, qui disent tous deux « minion ».
#  - « from THAT scheme » : le bonus va sur le complot DEJA choisi, pas sur un
#    second choix. Une seule cible, un seul retrait, dont le montant est
#    calcule avant.

BASE = 2


def GetAbilities() -> Sequence['Ability']:

    def murderous_glare(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        montant = BASE + SbiresVaincusCeRound(effect)
        this.RemoveThreatFromSchemes(effect.targets, montant, effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Enemy,
            murderous_glare,
            is_from_attack=True,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2, range=(1, 1)),
    ]
