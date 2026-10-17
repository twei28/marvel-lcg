from . import *

# Lookout — AMELIORATION 2 [mental], aspect Protection (TMNT Aspects, Inkwire). NYC. PREPARATION.
# Reduce the cost to play this card by 1 if you control a [[NYC]] support.
# Hero Response: After a minion engages you, discard Lookout -> cloak your hero and draw 1 card.
#
# NOUVELLE. MOT-CLE (fiches lues AVANT le code) : CLOAK (cloak.md) -> carte d'etat Cloaked (cloaked.md).
#
# CARTES DE REFERENCE
#  - `nt005` Kickflip : `ReduceCostToPlayThis(1, conditions=[...])` pour « Reduce the cost ... by 1 if ... ».
#  - `ua015` Demolish : « you control a NYC support » = `joueur.IsControl(CardFinder2("NYC", Support))`.
#  - `13017` Lie in Wait : `AfterMinionEngagePlayer(HeroResponse, None, "You", ...)` +
#    `.SetCostFunc(CostFunc.Discard("This"))` (PREPARATION defaussee comme cout).
#  - `td005` : « cloak » = `Faces.GiveStatus([...], "Cloaked", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « if you control a NYC SUPPORT » : un soutien au trait NYC, controle par le joueur (pas un allie, pas
#    une amelioration ; Lookout lui-meme, NYC mais amelioration, ne compte pas).
#  ⚠ « After a minion engages YOU » : `"You"`, n'importe quel sbire.
#  ⚠ « discard Lookout -> » : cout ; « cloak your HERO AND draw 1 card » : les deux, sur le heros (la
#    Reponse est une Hero Response : l'identite est en forme heros).
#  ⚠ Amelioration sans « Attach to » : posee devant le joueur (`CanPlayThisUpgradeCard()`).


def ControleUnSoutienNYC(effect: 'Effect', message: 'Message2') -> bool:
    Unused(message)
    joueur = effect.GetInitiator()
    return joueur is not None and joueur.IsControl(CardFinder2("NYC", Support))


def GetAbilities() -> Sequence['Ability']:

    def lookout(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is not None:
            Faces.GiveStatus([heros], "Cloaked", effect)
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.ReduceCostToPlayThis(
            1,
            conditions=[ControleUnSoutienNYC],
        ),
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.HeroResponse,
            None,
            "You",
            lookout,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
