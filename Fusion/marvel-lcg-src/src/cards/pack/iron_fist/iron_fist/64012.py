from . import *

# Redirect Chi — AMELIORATION, cout 0, [wild]. TECHNIQUE. x1 (Iron Fist 15/15).
# Temporary.
# Hero Resource: Remove 2 chi counters from Iron Fist -> generate [wild] [wild] resources.
#
# CARTES DE REFERENCE
#  - Hero Resource payee en compteurs d'une AUTRE carte : `phoenix/34001a` Phoenix
#    (`CanGenerateResources(HeroResource, Resources("G")).SetCostFunc(CostFunc.Counter(...))`).
#  - cout sur l'identite : `venus/tv001b` (`CostFunc.Counter("YourIdentity", ...)`).
#  - RECETTES §4 : UNE SEULE CanGenerateResources par carte ; un cout qui peut echouer se double
#    d'une `conditions` (sinon la ressource est offerte puis le paiement annule toute la carte).
#
# TEXTE CONTRE CODE
#  ⚠ Icone : l'etoile noire « ✱ ✱ » du texte est le glyphe [wild] (meme glyphe que 60043 American
#    Sign Language, Fear No Evil 2026, `generate a [wild]`) ; l'icone de ressource imprimee de la
#    carte (etoile verte) est identique a celle de 62002 Jessica Jones (`RES=G`) : wild.
#  ⚠ « Remove 2 chi counters from Iron Fist -> » : COUT de 2 sur l'identite, forme heros.
#  ⚠ DEUX ressources wild d'un coup (`Resources("GG")`).
#  ⚠ Temporary : base automatique ; perdu tant que Danny Rand est face visible (64001b).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("GG"),
            conditions=[AuMoinsChi(2)],
        ).SetCostFunc(CostFunc.Counter("YourIdentity", 2, CHI)),
    ]
