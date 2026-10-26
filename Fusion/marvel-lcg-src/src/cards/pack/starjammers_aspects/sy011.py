from . import *
# * Standing Still (Basic, soutien 3 [mental]). LOCATION. PLANET.
# Resource: Exhaust Standing Still → generate a [wild] resource for a player whose identity has the OUTLAW or STARJAMMER trait.
#
# Cartes de reference : as022 Spider-Verse (`CanGenerateResources(Resource, Resources(..), ..).SetCostFunc(Exhaust("This"))
# .AnyPlayerCanDoThis()` ; « Action » imprimee, `AbilityType.Resource` ecrit : ecart technique du GUIDE §9) ; la fabrique a deja
# `for_player_whose_identity_has_trait`, mais pour UN trait : ici DEUX (« OUTLAW or STARJAMMER »), d'ou une condition ecrite.
# « for a player whose identity has the trait » : le joueur qui PAIE (`message.GetToPlayer()`), pas forcement le proprietaire :
# `AnyPlayerCanDoThis()` + la condition de trait. Sans trait, la ressource n'est pas offerte meme a son proprietaire.
# ⚠ Une seule `CanGenerateResources` par carte. « a [wild] resource » : `Resources("G")`.
def GetAbilities() -> Sequence['Ability']:
    def outlaw_ou_starjammer(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity() if joueur is not None else None
        return identite is not None and (identite.HasTrait("OUTLAW") or identite.HasTrait("STARJAMMER"))
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            conditions=[outlaw_ou_starjammer],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]
