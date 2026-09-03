from . import *

# * Octo Spidey — Peter Parker (Earth-11983). Allie BASIC, x1. VARIANT.
# WEB-WARRIOR. Cout 4, PV 3, CTR 0*, ATQ 1*, ressource [wild].
# [star] Interrupt: When Octo Spidey uses a basic power, discard the top 4
#   cards of your deck. Octo Spidey gets +1 to that power for this use for
#   each different resource type discarded this way.
#
# Cartes de reference :
#  - **`32177` Swagger** et `im013` Tactical Interface (pack
#    iron_man_model_42) : `WhenUnitUseBasicPower(Interrupt, "This", op)` puis
#    `message.GainValue(n, effect)`, qui redirige tout seul vers le bon
#    pouvoir (sender_unit.py:21). C'est ce qui rend « +1 **to that power** »
#    sans avoir a lire lequel.
#  - **`16152`** Contingency Plan : `player.DiscardDeckTopCards(4, effect)`
#    puis `FacesCounter.GetPrintedResourcesTypes(faces)`. MEME phrase
#    (« for each different resource type discarded this way »), meme nombre
#    de cartes.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « uses **a basic power** », sans preciser lequel : attaque, menee,
#    defense et recuperation, TOUS. Aucun filtre `powers=`, contrairement a
#    im013 qui imprime « makes a basic **thwart** ».
#  - « +1 to **that** power **for this use** » : le bonus ne vaut que pour
#    l'utilisation en cours. `GainValue` porte deja cette portee ; un
#    `GainUntilRoundEnd` serait faux.
#  - « for each **different resource type** » : les types DISTINCTS parmi les
#    4 cartes defaussees (4 au maximum), pas le nombre de cartes.
#    `GetPrintedResourcesTypes`, jamais `len(faces)`.
#  - « **your** deck » : le deck du joueur qui controle Octo Spidey, pas le
#    proprietaire de la carte si elle a change de mains.
#  - « [star] » sans « In expert mode » : capacite TOUJOURS active, convention
#    moteur (cf. 04125). Rien a conditionner.
#  - ⚠ CTR imprimee **0** : Octo Spidey ne menace a rien sans cette capacite.
#    Le pack le sait — c'est une carte a jouer pour ses pouvoirs gonfles, pas
#    pour ses statistiques.


def GetAbilities() -> Sequence['Ability']:

    def octo_spidey(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Unused(this)

        faces = joueur.DiscardDeckTopCards(4, effect)
        types = FacesCounter.GetPrintedResourcesTypes(faces)
        if types <= 0:
            return
        message.GainValue(types, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            octo_spidey,
        ),
    ]
