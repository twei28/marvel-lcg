from . import *

# Number Cruncher (Support, reecriture a 3 couts de l'original officiel, pour la restriction de deck de 3-D Man)
#
# Max 1 per player.
# Interrupt: When you discard a 3-cost event from your hand to pay for another event, exhaust this card ->
#   triple the number of resources that card generates.
#
# CARTES DE REFERENCE
#  - `sy015` Stolen Goods : modele d'une carte "Resource: Discard this card -> generate [wild][wild]" -- le genre
#    de carte que dm017 cible ("a 3-cost event" qui genere des ressources en se defaussant).
#  - `yd007` Jackpot! (Resource signature) : MEME MECANIQUE DE BASE ("treat the next card you spend as if it has
#    double the resources") -> `AbilityFactory.AfterGenerateResources(AbilityType.Rule, "You", op)` sur
#    `Message.WhenCardBeSpendAsResource` (la fenetre envoyee par `DoGenerateResources` JUSTE APRES que la carte
#    depensee a verse ses ressources dans `res_pool`) : on y reverse `message.res` dans `res_pool` pour chaque
#    multiplicateur supplementaire voulu (+1x pour "double", ici +2x pour "triple" -- le 1x initial est deja
#    verse par le moteur avant que ce message parte). PAS une interception avant generation : le moteur n'offre
#    pas de "would generate" modifiable ici, la multiplication se fait en ajoutant le meme montant apres coup,
#    ce qui donne le meme total final.
#  - `an006` Angelic Ribbons : "exhaust this card" est le COUT -> `CostFunc.Exhaust("This")`.
#
# TEXTE CONTRE CODE
#  "a 3-COST event" : `message.trigger` (la carte depensee) est un Event ET son `printed_cost.val == 3`.
#  "from your hand" : aucune autre carte du kit ne permet de depenser un evenement comme ressource autrement
#    que depuis la main (mecanique "Resource: discard this card" standard, toujours jouee depuis la main) -> pas
#    de condition de provenance distincte a coder, comme dm007/dm008 dans ce meme pack.
#  "to pay for ANOTHER event" : `message.pay_for_card` doit etre un Event (pas une amelioration/allie/soutien).
#  "triple THE NUMBER OF RESOURCES that card generates" : le TOTAL final doit valoir 3x, pas +3 -> 2 versements
#    supplementaires de `message.res` (1x deja verse par le moteur + 2x ici = 3x).
#  "Max 1 per player" -> `desc.MaxPerUnit` ("1"), lu nativement, aucun code necessaire.

def GetAbilities() -> Sequence['Ability']:

    def evenement_3_couts_pour_un_autre_evenement(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> bool:
        if not Event.IsType(message.trigger):
            return False
        if message.trigger.printed_cost.val != 3:
            return False
        return Event.IsType(message.pay_for_card)

    def number_cruncher(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        joueur.res_pool.Gain(message.res, effect)
        joueur.res_pool.Gain(message.res, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.AfterGenerateResources(
            AbilityType.Interrupt,
            "You",
            number_cruncher,
            conditions=[evenement_3_couts_pour_un_autre_evenement],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
