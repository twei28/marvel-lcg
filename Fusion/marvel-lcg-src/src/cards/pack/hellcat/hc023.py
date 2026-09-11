from . import *
# Chase Them Down — EVENEMENT d'AGRESSIVITE, cout 0, [mental]. THWART.
# Response (thwart): After your hero attacks and defeats an enemy, remove 2
#   threat from a scheme.
#
# RESKIN de 01052 (art de jakxin, texte identique) : doublon voulu par
# l'utilisateur le 11/09/2026. Module copie de core/01052.py, ligne pour
# ligne.

def GetAbilities() -> Sequence['Ability']:

    def chase_them_down(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.Response,
            "YourHero",
            Enemy,
            chase_them_down,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
