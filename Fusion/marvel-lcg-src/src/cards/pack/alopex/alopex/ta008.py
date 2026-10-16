from . import *

# * Kitsune Kabuki — AMELIORATION signature, x1. ITEM. MYSTIC.
# Cout 3, [mental].
# Each hunter counter on this card can be spent as if it were a [mental]
#   resource.
# Hero Response: After Prey leaves play, place 1 hunter counter here.
#
# Cartes de reference :
#  - « each X counter can be spent as if it were a [Y] resource » :
#    `raphael/tr001a` et `30001a` * Spider-Ham : `CanGenerateResources(type,
#    Resources("B")).SetCostFunc(CostFunc.Counter("This", 1, 'hunter'))
#    .SetToAvailableTimesFn(...)` ;
#  - « After <carte> leaves play » : `AfterCardLeavePlay(type, finder, op)`
#    (card_move.py:258) ; pose d'un compteur : `Faces.PlaceCountersOn`.
#
# Mots-pieges :
#  - « [MENTAL] » et pas wild : `Resources("B")` (icone verifiee par decoupe,
#    voir le gabarit) ;
#  - le compteur `hunter` est pose sur CETTE carte (« here »), pas sur Alopex ;
#  - « Hero Response » : forme heros ; « After PREY leaves play » : la carte
#    Prey (ta011), qu'elle parte par defaite de sa cible, retrait de la
#    manigance, defausse... ; la ressource, elle, marche dans les DEUX formes ;
#  - « Each ... counter » : un compteur = une ressource, `ToAvailableTimesFn`
#    en donne le nombre ;
#  - le type de la ressource est `Resource` (le texte n'est pas une capacite de
#    heros : la forme alter-ego peut aussi depenser les compteurs).


def GetAbilities() -> Sequence['Ability']:

    def poser_un_compteur(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, HUNTER, effect)

    def chasseurs_disponibles(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> int:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        return this.GetCounters(HUNTER)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B"),
        ).SetCostFunc(CostFunc.Counter("This", 1, HUNTER))
        .SetToAvailableTimesFn(chasseurs_disponibles),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.HeroResponse,
            CardFinder(name=NOM_PREY),
            poser_un_compteur,
        ),
    ]
