from . import *

# Guerilla Trap — AMELIORATION 2 [energy], aspect Aggression (TMNT Aspects, Inkwire). NYC. PREPARATION.
# Reduce the cost to play this card by 1 if you control a NYC support.
# Hero Response: After a minion engages you, discard Guerilla Trap → daze that minion and cloak your hero.
#
# MOTS-CLES (fiches lues AVANT le code) : daze.md (« daze » = poser la carte d'etat Dazed), cloak.md
#   (« cloak » = poser la carte d'etat Cloaked).
# CARTES DE REFERENCE
#  - `13017` Lie in Wait : « After a minion engages you, discard Lie in Wait → deal 3 damage to that minion » =
#    `AfterMinionEngagePlayer(HeroResponse, None, "You", ...)` + `CostFunc.Discard("This")` + `SetTarget("Trigger")`.
#  - `ua015` Demolish : « If you control a NYC support » = `IsControl(CardFinder2("NYC", Support))`.
#  - `ReduceCostToPlayThis(1, conditions=[...])` (resources.py) : reduction du cout de CETTE carte.
#  - `ta002` (Alopex) : `Faces.GiveStatus(..., "Dazed" | "Cloaked", effect)`.
# TEXTE CONTRE CODE
#  ⚠ « that minion » = le sbire qui vient d'engager (Trigger) ; « YOUR HERO » = l'identite en forme heros
#    (Hero Response : jouable en forme heros seulement).
#  ⚠ « daze AND cloak » : les deux.


def ControleUnSoutienNYC(effect: 'Effect', message: 'Message2|None' = None) -> bool:
    Unused(message)
    joueur = effect.GetInitiator() or effect.this.GetControlByOrOwner()
    return joueur is not None and Player.IsType(joueur) and joueur.IsControl(CardFinder2("NYC", Support))


def GetAbilities() -> Sequence['Ability']:

    def piege(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        Faces.GiveStatus(effect.targets, "Dazed", effect)
        heros = effect.GetInitiator().GetHero()
        if heros is not None:
            Faces.GiveStatus([heros], "Cloaked", effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[ControleUnSoutienNYC]),
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.HeroResponse,
            None,
            "You",
            piege,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("Trigger"),
    ]
