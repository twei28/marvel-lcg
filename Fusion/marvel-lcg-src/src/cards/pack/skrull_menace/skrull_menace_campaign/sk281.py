from . import *

# Skrull Battleship — SOUTIEN de campagne (Leadership / Campaign, n° 281). Cout 2. NON unique. SKRULL. VEHICLE.
# Play only if you control a SKRULL ally.
# Hero Resource: Exhaust Skrull Battleship -> generate a [wild] resource for any player.
#
# Cartes de reference :
#  - **`fne/60043`** American Sign Language : « Hero Resource: Exhaust this card -> generate a [wild] resource for
#    ... any player » = `CanGenerateResources(HeroResource, Resources('G')).SetCostFunc(Exhaust("This"))
#    .AnyPlayerCanDoThis()`.
#  - **`sm/27017`** Spider-Man (hobie) : « Play only if you control a X » ; ici la condition est posee sur la
#    fabrique de jeu des SOUTIENS (`CanPlayThisSupportCard(conditions=[...])`).
#
# ⚠ Mots-pieges :
#  - « Play only if you control a SKRULL ALLY » : un ALLIE (pas un sbire, pas un soutien SKRULL) que VOUS controlez
#    (pas un allie d'un autre joueur) ; la condition ne porte que sur le JEU de la carte, pas sur son maintien ;
#  - « Hero RESOURCE » : generation de ressource, forme heros ; « FOR ANY PLAYER » : n'importe quel joueur peut
#    s'en servir pour payer (`AnyPlayerCanDoThis`) ; « wild » = une ressource de n'importe quelle couleur ;
#  - Pas de limite « max 1 » imprimee : plusieurs exemplaires possibles (carte non unique).


def GetAbilities() -> Sequence['Ability']:

    def controle_un_allie_skrull(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        joueur = effect.GetInitiator()
        return joueur is not None and len(LesAlliesSkrull(joueur)) > 0

    return [
        AbilityFactory.CanPlayThisSupportCard(conditions=[controle_un_allie_skrull]),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")).AnyPlayerCanDoThis(),
    ]
