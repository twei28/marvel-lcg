from . import *

# * Angela (face heros)
# ASGARD. GUARDIAN.  THW 1 / ATK 2 / DEF 2 — HS 4 / PV 13
# Frenzy - Response: After you defeat a minion, ready Angela.
#   (Limit once per round.)
#
# Cartes de reference : vp001a Fear Factor (pack venompool) pour le montage
# `AfterUnitDefeatedUnit(Response, "You", <cible>, ...)`, 60054 Stand Alone
# pour `Faces.ReadyAll([identite], effect)`.
#
# ⚠ « defeat a MINION », pas « an enemy » : le troisieme argument est Minion
# et non Enemy. Le contraste est visible dans le pack lui-meme — an004
# Murderous Glare dit « defeats an ENEMY », donc le vilain compte pour elle et
# pas pour celle-ci.

def GetAbilities() -> Sequence['Ability']:

    def frenzy(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        identite = initiator.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            frenzy,
        ).SetName("Frenzy")
        .LimitOncePerRound(),
    ]
