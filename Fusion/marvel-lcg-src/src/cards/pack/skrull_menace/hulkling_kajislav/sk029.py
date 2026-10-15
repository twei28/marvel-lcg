from . import *

# Glorious Flight — amelioration d'aspect BASIC (n° 29). PREPARATION.
# Cout 1 [energy].
# Play only if you have an [[AERIAL]] trait.
# Hero Response: After you defeat an enemy or a side scheme, discard Glorious
#   Flight → ready your hero.
#
# Cartes de reference :
#  - **`47018`** * Synch : « Play only if your identity has the X trait » =
#    `CanPlayThis...().SetPlay(only_if_your_identity_has_trait=...)`.
#  - **`52001a`** * Silk : « After you defeat a minion or side scheme » =
#    `AfterUnitDefeatedUnit(Response, "You", <type>, op)` +
#    `AfterUnitDefeatedScheme(Response, "You", SchemeSide2, op)`.
#  - `50042` EM Shield pour le cout `CostFunc.Discard("This")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Play only if **you** have AERIAL » : condition de JEU seulement ; une
#    fois en jeu, perdre AERIAL ne la defausse pas.
#  - « an **enemy** or a **side scheme** » : sbire ou vilain (`Enemy`), et
#    complot ANNEXE (`SchemeSide2`), pas le principal.
#  - « **you** defeat » : toi ou une carte que tu controles (fabrique "You").
#  - « discard Glorious Flight → » : cout, usage unique.
#  - « **Hero** Response ».


def GetAbilities() -> Sequence['Ability']:

    def envol(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        Faces.ReadyAll([effect.GetInitiator().GetIdentity()], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
        ).SetPlay(only_if_your_identity_has_trait="AERIAL"),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Enemy,
            envol,
        ).SetCostFunc(CostFunc.Discard("This")),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.HeroResponse,
            "You",
            SchemeSide2,
            envol,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
