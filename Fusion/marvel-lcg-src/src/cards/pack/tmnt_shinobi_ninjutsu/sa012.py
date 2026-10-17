from . import *

# Black Ops — AMELIORATION 1 [physical], Ninjutsu (TMNT Shinobi, Inkwire). Aucun trait.
# Hero Action: After your hero defeats a minion or side scheme, discard Black Ops -> ready your hero.
# « That's one less obstacle... » —Raphael
#
# ⚠ QUESTION Q-N2 RESOLUE le 17/10/2026 (reponse : Hero RESPONSE) (.planning/tmnt/shinobi-ninjutsu-questions.md) : « Hero ACTION: AFTER ... » est
# contradictoire (une Action se joue a volonte, « After » est le declencheur d'une REPONSE ; meme coquille que The Made
# Men, ud004). Lecture retenue : Hero RESPONSE, comme `se008` Onigari (« After you defeat a
# minion or side scheme »). Carte terminee.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : aucun (pas de Cloak sur le texte imprime).
#
# Cartes de reference :
#  - `se008` Onigari : « After you defeat a minion OR side scheme » = DEUX capacites, `AfterUnitDefeatedUnit(.., "You",
#    Minion, fn)` + `AfterUnitDefeatedScheme(.., "You", SchemeSide2, fn)` ;
#  - `13017` Lie in Wait / `up023` Lookout : « discard <cette carte> -> » = `.SetCostFunc(CostFunc.Discard("This"))` ;
#  - `09015` : « ready your hero » = `Faces.ReadyAll([hero], effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « AFTER YOUR HERO defeats » : le heros du joueur (pas un allie) ; « a MINION OR SIDE scheme » : un sbire ou un
#    complot annexe (ni le vilain, ni le complot principal) ; « discard Black Ops -> » est le COUT.
#  ⚠ Le heros peut etre incline ou non ; « ready your hero » : le redresse.


def GetAbilities() -> Sequence['Ability']:

    def black_ops(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        Faces.ReadyAll([joueur.GetHero()], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Minion,
            black_ops,
        ).SetCostFunc(CostFunc.Discard("This")),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.HeroResponse,
            "You",
            SchemeSide2,
            black_ops,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
