from . import *

# * Doom's Mask — amelioration signature. TECH. Cout 3.
# Doctor Doom gains steady.
# Resource: Exhaust Doom's Mask -> generate a [mental] resource
#   ([mental][mental] resources instead if paying for a SPELL event).
#
# Cartes de reference :
#  - « gains steady » : `GiveKeywordToAttached("You", steady=1)` (recette §3,
#    fiche docs/reference/mots-cles/steady.md) ;
#  - ressource variable selon la carte payee : an007, `resources_fn=fn`
#    evaluee AU PAIEMENT (recette moteur §4) ;
#  - couple inclinaison + generation : ab007 * Donald Pierce.
#
# ⚠ PIEGE ho009, deja paye : dans le couple Can+Do de 31001a, `res` est FIGE
# avant le `PayCost`. On n'utilise donc PAS ce montage mais `resources_fn`,
# qui recoit le message de verification et peut lire la carte reellement
# payee. La couleur, elle, ne change pas : seule la QUANTITE double.
#
# ⚠ UNE SEULE `CanGenerateResources` par carte (assert du moteur) : la
# variante « double pour un SPELL » doit donc vivre DANS la fonction, pas dans
# une seconde fabrique.

def GetAbilities() -> Sequence['Ability']:

    def ressource_selon_la_carte(effect: 'Effect',
                                 message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        Unused(effect)
        # ⚠ Le champ est `paying_for_card` (sender_player.py:281), la carte
        # qu'on est en train de payer. Il vaut None quand le paiement ne vise
        # pas une carte joueur (capacite, cout d'effet) : on retombe alors sur
        # la ressource simple.
        face = message.paying_for_card
        double = face is not None and Event.IsType(face) and face.HasTrait("SPELL")
        return Resources("BB") if double else Resources("B")

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            steady=1,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=ressource_selon_la_carte,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
