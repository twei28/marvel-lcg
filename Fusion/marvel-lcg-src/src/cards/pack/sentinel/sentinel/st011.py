from . import *

# Propulsion Array — Amelioration 0 [energy], classe Hero.
# [star] As an additional cost to play this upgrade, exhaust Legs (Intact).
# Hero Action: Shuffle this card into your deck. Choose one:
#  • Exhaust 1 [[COMPONENT]] ([[INTACT]] side up) upgrade → ready Sentinel.
#  • Exhaust Sentinel → ready up to 2 [[COMPONENT]] ([[INTACT]] side up)
#    upgrades.
#
# Cartes de reference :
#  - `56007` Hunted : une amelioration dont la capacite de JEU porte un cout
#    additionnel, `CanPlayThisUpgradeCard().SetCostFunc(...)`.
#  - `61005` Infiltration : `Faces.ShuffleAllTo([this], joueur.player_deck, e)`.
#  - `aa005` / `dz037` : `ChooseAbilities` pour un « Choose one » obligatoire.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Shuffle this card into your deck** » est la PREMIERE instruction de
#    l'effet, pas un cout : la carte part meme si la branche choisie ne fait
#    rien. On remelange donc AVANT de proposer le choix.
#  - Les deux branches ont chacune leur propre cout d'inclinaison. Une branche
#    dont le cout n'est pas payable ne doit pas etre proposee : c'est
#    `CostFunc.Exhaust` qui s'en charge, son selecteur exige `canbe_exhaust`.
#  - « ready **Sentinel** » : l'identite, en forme heros (c'est une action de
#    heros). « up to 2 » : zero, une ou deux, d'ou `("Zero", 2)`.
#  - Les deux branches ne visent que des Component **INTACT** : une piece
#    detruite n'a plus d'action a redresser.
#  - Cout imprime ZERO : la carte se rejoue a volonte, et c'est la duree de vie
#    des Legs qui la borne.


def GetAbilities() -> Sequence['Ability']:

    def propulsion_array(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = effect.GetInitiator()
        Faces.ShuffleAllTo([this], joueur.player_deck, effect)

        def redresser(cibles: Sequence['CardFace'], e: 'Effect') -> None:
            Faces.ReadyAll(cibles, e)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility3(
                "Exhaust 1 COMPONENT upgrade -> ready Sentinel", redresser)
            .SetCostFunc(CostFunc.Exhaust(SelecteurComposantIntact()))
            .SetTarget("YourIdentity", canbe_ready=True),
            AbilityFactory.ForChoiceAbility3(
                "Exhaust Sentinel -> ready up to 2 COMPONENT upgrades", redresser)
            .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetTarget(
                Upgrade,
                trait=TRAIT_INTACT,
                canbe_ready=True,
                from_where=["YouControlCards"],
                range=("Zero", 2),
            ),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard()
        .SetCostFunc(CostFunc.Exhaust(SelecteurComposantIntact(nom=NOM_LEGS))),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            propulsion_array,
        ),
    ]
