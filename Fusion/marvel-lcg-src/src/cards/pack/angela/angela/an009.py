from . import *

# * Xiphos (Sword of the Stars) — amelioration. ASGARD. WEAPON. Cout 2.
# Restricted.
# Angela gets +1 ATK.
# Response: After Angela defeats a minion, draw a card. (Limit once per round.)
#
# Cartes de reference : 05023 Endurance / ra007 Mjolnir pour le +1 ATK attache,
# an001a Frenzy (meme pack) pour le declencheur `AfterUnitDefeatedUnit` sur un
# Minion avec `.LimitOncePerRound()`.
#
# « Restricted » est lu directement dans `desc` (Restricted: "1"), AUCUN module
# n'est necessaire — voir PROCESSUS-CARTE etape 5, « bases automatiques ».

def GetAbilities() -> Sequence['Ability']:

    def xiphos(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is not None:
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            attack=1,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            xiphos,
        ).LimitOncePerRound(),
    ]
