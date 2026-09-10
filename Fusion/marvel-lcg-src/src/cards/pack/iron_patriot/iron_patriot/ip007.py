from . import *

# * H.A.M.M.E.R. Helicarrier — SOUTIEN, cout 3, RES [energy].
# H.A.M.M.E.R. VEHICLE.
# Increase your ally limit by 1. (This allows you to control more than 3 allies.)
# Action: Exhaust this card and spend 1 resource of any type -> ready a
#   REGISTERED ally.
#
# ⚠⚠ LE ZIP CONTIENT DEUX VERSIONS DE CETTE CARTE, meme numero imprime (6/16),
# differentes sur 96 % de l'image : l'une dit « Action », l'autre « Response ».
# On retient l'ACTION. Deux raisons : le fichier suit la numerotation
# zero-padee de tout le dossier, et surtout un « Response » sans clause
# « After... » n'est pas une Reponse valide dans les regles du jeu. L'autre
# fichier est un brouillon laisse dans le zip.
#
# CARTE DE REFERENCE
#  - `03024` * Avengers Tower : « increase your ally limit by 1 », par le
#    parametre `ally_limit` de `GiveKeywordToInPlayWhenApplyThis`.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX couts avant la fleche : l'inclinaison ET une ressource. Deux
#    `SetCostFunc` chaines.
#  ⚠ « ready a REGISTERED ALLY » : un allie deja pret n'est pas une cible
#    valable, d'ou `canbe_ready=True`.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        Faces.ReadyAll([c for c in effect.targets if c is not None], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            control_by="You",
            ally_limit=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            redresser,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Spend(Cost("1")))
        .SetTarget(CardFinder(trait=TRAIT_REGISTERED, card_type=Ally),
                   canbe_ready=True),
    ]
