from . import *

# * Gwen Stacy (Earth-31198) — soutien signature, x1. PERSONA. Cout 3,
# ressource [mental].
# Response: After a card with the printed cost of 2 or more enters play under
#   your control, ready Gwen Stacy. (Limit once per round.)
# Resource: Exhaust Gwen Stacy -> generate a [wild] resource.
#
# Cartes de reference :
#  - **`17022`** * Knowhere : `AfterPlayerPlayedCard`/`AfterCardEnterPlay` +
#    `CostFunc.Exhaust("This")`, meme forme de soutien qui reagit a l'arrivee
#    d'une carte.
#  - **`ab007`** * Donald Pierce (pack albert, meme auteur Kajislav) et
#    `ma005` : `CanGenerateResources(AbilityType.Resource, Resources("G"))
#    .SetCostFunc(CostFunc.Exhaust("This"))`. C'est le montage canonique du
#    « Resource: Exhaust -> generate a [wild] ».
#  - `an001a` / `ok014` pour `Faces.ReadyAll([this], effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **enters play** », pas « is played » : une carte mise en jeu par un
#    autre effet (fouille, mise en place, capacite d'un allie) compte aussi.
#    D'ou `AfterCardEnterPlay` et non `AfterPlayerPlayedCard`, qui exigerait
#    un vrai `Play`.
#  - « **printed** cost of 2 or more » : le cout IMPRIME. Une reduction de
#    cout ne change rien, et une carte sans cout imprime ne compte pas
#    (helper `CoutPrintedAuMoins`).
#  - « under **your** control » : `under_your_control=True`, qui compare
#    `message.trigger.GetControlBy()` a l'initiateur.
#  - « (Limit once per round.) » : limite GLOBALE, pas par joueur — c'est
#    l'inverse exact de as001b Egomaniac, qui imprime « per player ».
#    `LimitOncePerRound()`, et surtout pas `LimitOncePerRoundPerPlayer()`.
#  - ⚠ Gwen Stacy coute 3 : en entrant en jeu elle declenche sa PROPRE
#    reponse. C'est bien ce qui est imprime (« a card », sans exclusion),
#    et le redressement est alors sans effet puisqu'elle arrive redressee.
#  - ⚠ **UNE SEULE `CanGenerateResources` par carte** (assert du moteur).


def GetAbilities() -> Sequence['Ability']:

    def gwen_stacy(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            CardFace,
            gwen_stacy,
            under_your_control=True,
            conditions=[
                lambda effect, message: CoutPrintedAuMoins(message.trigger, 2),
            ],
        ).LimitOncePerRound(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
