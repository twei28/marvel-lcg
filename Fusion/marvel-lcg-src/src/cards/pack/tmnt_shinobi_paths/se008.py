from . import *

# Onigari — PATH hybride (avance), classes Kuji-Kiri + Ninjutsu (Inkwire, TMNT Shinobi). KUJI-KIRI. NINJUTSU.
# Permanent. You get -1 hand size. You gain the PSIONIC trait.
# Dark Visions — Hero Response: After you defeat a minion or side scheme, exhaust this card -> cloak your hero
#   and draw 1 card.
#
# Mots-cles (fiches lues AVANT le code) : Cloak (cloak.md) ; Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « After you defeat a minion OR side scheme » : `skrull_menace/hulkling_kajislav/sk029` / `52001a` Silk =
#    `AfterUnitDefeatedUnit(HeroResponse, "You", Minion, op)` + `AfterUnitDefeatedScheme(HeroResponse, "You",
#    SchemeSide2, op)` ; cout `CostFunc.Exhaust("This")` (04160b) ;
#  - « cloak your hero and draw 1 card » : `tmnt_aspect_protection/up023` Lookout.
#
# TEXTE CONTRE CODE
#  ⚠ « you defeat a MINION or SIDE scheme » : un SBIRE (pas le vilain, pas un allie) ou un complot ANNEXE (pas le
#    principal) ; « YOU defeat » : par vous ou une carte que vous controlez ("You").
#  ⚠ « cloak your hero AND draw 1 card » : les deux ; un heros deja camoufle ne recoit pas de seconde carte mais
#    pioche quand meme.
#  ⚠ « Hero Response » : forme heros ; cout : incliner la carte (deux capacites, UN seul redressement).


def GetAbilities() -> Sequence['Ability']:

    def dark_visions(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        ShinobiCloak(effect, joueur.GetHero())
        joueur.DrawUp(1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1, trait="PSIONIC"),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Minion,
            dark_visions,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.HeroResponse,
            "You",
            SchemeSide2,
            dark_visions,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
