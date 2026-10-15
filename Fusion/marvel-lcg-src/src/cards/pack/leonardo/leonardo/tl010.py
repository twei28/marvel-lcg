from . import *

# Nukitsuke — AMELIORATION signature, x1. STANCE. Cout 2, [mental].
# Hero Action: Exhaust Nukitsuke -> ready a [[KATANA]] upgrade you control.
#
# Cartes de reference :
#  - `ho009` Goblin Helmet / `31009` SP//dr Command : `HeroAction` payee par
#    `CostFunc.Exhaust("This")`, cible `SetTarget(Upgrade, trait=...,
#    from_where=["YouControlCards"], canbe_ready=True)` + `Faces.ReadyAll`.
#
# Mots-pieges :
#  - « a [[KATANA]] upgrade YOU CONTROL » : `YouControlCards` ;
#  - `canbe_ready=True` : sans cible legale (tous les katanas prets) la
#    capacite n'est pas proposee ;
#  - Nukitsuke n'est PAS un KATANA : elle ne peut pas se redresser elle-meme.


def GetAbilities() -> Sequence['Ability']:

    def nukitsuke(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Faces.ReadyAll(list(effect.targets), effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            nukitsuke,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Upgrade, trait="KATANA", from_where=["YouControlCards"],
                   canbe_ready=True),
    ]
