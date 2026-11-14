from . import *

# * Screwball — SBIRE UNIQUE. CONTENT CREATOR. CRIMINAL. SCH 2, ATQ 1, 3 PV, Boost 1, Hazard 1.
# Forced Interrupt : When Screwball would be defeated with excess damage, reset her hit points instead. Attach her to an unoccupied location, if
#   able. (She remains in play.)
# Forced Interrupt : When a player enters Screwball's location, she engages them.
#
# Cartes de reference : fne/typhoid_mary (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `ResetHealth`), pu013 (attache / engage),
# `Message.WhenUnitWouldBeDefeated.excess_damage` (nouveau, can_health.py).
# ⚠ « with EXCESS damage » : seulement si le coup depasse ses PV restants (un coup EXACT la vainc normalement) ; « reset her hit points instead » :
# PV au maximum (3) ; « if able » : sans lieu libre elle reste engagee, PV remis quand meme.

def GetAbilities() -> Sequence['Ability']:

    def avec_exces(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        return message.excess_damage > 0

    def reapparait(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = SbireEngagePar(this)
        message.SetBeInstead(effect)
        this.ResetHealth(effect)
        AttacherAuLieuInoccupe(effect, this, joueur)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, "This", reapparait, conditions=[avec_exces]),
        EngageQuandOnEntreDansSonLieu(),
    ]
