from . import *

# * Dragon Scale — AMELIORATION, cout 2, [wild]. ARTIFACT. ELEMENT. MYSTIC. x1.
# Resource: Exhaust this card and remove 1 dredge counter from Venus -> generate a
#   [wild] resource.
#
# CARTES DE REFERENCE
#  - `tr001a` Raphael (pack raphael) : `CanGenerateResources(...)` dont le cout est un
#    compteur maison de l'identite (`CostFunc.Counter(...)`), `ab007` / `ma005` pour
#    « Resource: Exhaust -> generate [x] » (`CanGenerateResources(...).SetCostFunc(Exhaust)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Resource: » SANS « Hero » : utilisable aux DEUX formes. « Venus » = l'identite meme en
#    forme Bonnie (decision du 15/10/2026 pour « Raphael » en civil).
#  ⚠ « generate a [WILD] resource » -> `Resources("G")`, UNE seule (une seule
#    `CanGenerateResources` par carte, assert moteur).
#  ⚠ Deux couts : inclinaison ET 1 compteur. `conditions=[a_un_compteur]` est OBLIGATOIRE : sans elle la
#    ressource est OFFERTE au paiement meme sans compteur, le cout echoue et le moteur ANNULE toute la
#    carte en train d'etre payee (RECETTES §4, « ressource a cout Custom »). Cas : « sans compteur ».


def GetAbilities() -> Sequence['Ability']:

    def a_un_compteur(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        Unused(message)
        return PeutRetirerDragage(effect, 1)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            conditions=[a_un_compteur],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("YourIdentity", 1, DREDGE)),
    ]
