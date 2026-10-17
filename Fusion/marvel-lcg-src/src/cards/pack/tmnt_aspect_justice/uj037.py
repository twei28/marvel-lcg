from . import *

# Watch the Exits — AMELIORATION 2 [physical], aspect Justice (TMNT Aspects, Inkwire). NYC. PREPARATION.
# Reduce the cost to play this card by 1 if you control a [[NYC]] support.
# Hero Response: After a minion engages you, discard Watch the Exits → remove 2 threat from a scheme and
#   ready your hero.
#
# CARTES DE REFERENCE
#  - `fne` `DiscountAbility` (60023 / 60027) : reduction conditionnelle du cout de CETTE carte =
#    `AbilityFactory.ReduceCostToPlayThis(1, conditions=[...])`, le joueur lu par `GetControlByOrOwner()`.
#  - `ua015` Demolish : « you control a NYC support » = `joueur.IsControl(CardFinder2("NYC", Support))`.
#  - `27159` / `16118` : « After a minion engages you » = `AfterMinionEngagePlayer(type, <sbire>, "You", op)`.
#  - `sk029` Glorious Flight : « Hero Response ... discard <this> → ... ready your hero » =
#    `.SetCostFunc(CostFunc.Discard("This"))` + `Faces.ReadyAll([joueur.GetIdentity()], effect)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « Reduce the cost to play THIS card by 1 IF YOU CONTROL a NYC SUPPORT » : soutien NYC sous TON controle.
#  ⚠ « Hero Response » : forme heros seulement (sous-type dedie).
#  ⚠ « After a MINION engages YOU » : un sbire, qui s'engage avec TOI (pas un autre joueur).
#  ⚠ « discard Watch the Exits → » : FLECHE = COUT, usage unique.
#  ⚠ « remove 2 threat from a scheme AND ready your hero » : les deux.
#  Aucune limite imprimee.


def ControleUnSoutienNYC(joueur: 'Player|None') -> bool:
    return Player.IsType(joueur) and joueur.IsControl(CardFinder2("NYC", Support))


def GetAbilities() -> Sequence['Ability']:

    def surveiller(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        Faces.ReadyAll([effect.GetInitiator().GetIdentity()], effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(
            1,
            conditions=[lambda effect, message: ControleUnSoutienNYC(effect.this.GetControlByOrOwner())],
        ),
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.HeroResponse,
            Minion,
            "You",
            surveiller,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Scheme2),
    ]
