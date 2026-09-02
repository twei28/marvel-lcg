from . import *

# * Viv's Solar Gem — AMELIORATION signature, x1 (n/15 = 15). ITEM.
# Cout 2, ressource [energy]. PAS de Requirement imprime.
# Resource: Exhaust Viv's Solar Gem -> generate a [energy] resource.
# Response: After the villain phase ends, ready Viv's Solar Gem.
#
# Cartes de reference :
#  - sd015 Never Ending Spark (pack speed) : la MEME carte a un declencheur
#    pres — `CanGenerateResources(AbilityType.Resource, Resources("Y"))
#    .SetCostFunc(CostFunc.Exhaust("This"))` pour la ressource, et
#    `Faces.ReadyAll([this], effect)` pour le redressement. Ses modeles amont
#    (48005 Prehensile Tail, 54002 Cybernetic Arm) valent donc aussi ici ;
#  - 29030 * Lucia von Bardas (pack ironheart) pour « after the villain phase
#    ends » : `AfterPhaseEnd(<type>, "Villain", op)`.
#
# ⚠ UNE SEULE `CanGenerateResources` par carte : `ClassCard.GetAbilities`
# (card_player.py:83-84) leve un assert au-dela.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Resource: » nu, et non « Hero Resource: » : la ressource se genere
#    AUSSI en forme alter-ego, d'ou `AbilityType.Resource`. Meme lecture que
#    sd015. Ne pas « corriger » en HeroResource.
#  - « Response: » nu, et non « Hero Response: » : le redressement joue quelle
#    que soit la forme. C'est important ici, parce que la fin de phase du
#    vilain trouve souvent Viv en alter-ego.
#  - « generate A [energy] resource » : UNE seule, `Resources("Y")`.
#  - Aucune restriction sur ce que la ressource peut financer : le texte n'a
#    pas de « to pay for... », donc pas de `for_card=` (meme lecture que sd015,
#    contrairement a 48005 et 54002 qui, elles, l'impriment).
#  - « ready Viv's Solar Gem » : la carte elle-meme, pas une autre. Redresser
#    une carte deja prete ne fait rien et ne leve pas d'erreur.
#  - « After the VILLAIN phase ends » : la phase du vilain, pas la fin de
#    round. Concretement, la gemme redevient disponible AVANT la phase joueur
#    suivante — c'est ce qui permet de la depenser pour vv004 Phase Up pendant
#    la phase du vilain, puis de l'avoir a nouveau a son tour.


def GetAbilities() -> Sequence['Ability']:

    def redresser_la_gemme(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPhaseEnd(
            AbilityType.Response,
            "Villain",
            redresser_la_gemme,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("Y"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
