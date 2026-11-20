from . import *

# Tri-Power (Resource, [physical][mental][energy])
#
# Hero Response: After you spend this resource, ready 3-D Man.
#
# CARTES DE REFERENCE
#  - `56132` Suit Up (Resource, meme famille de texte) : `AbilityFactory.AfterYouSpendThisCard(AbilityType.
#    HeroResponse, op)`, message `Message.AfterCardsBeSpendAsResource`.
#  - `21183` Shawarma (RES multi-couleurs "RBY") : la generation des 3 ressources elle-meme est lue NATIVEMENT
#    par le moteur depuis `desc.RES` -- aucune capacite necessaire pour ca, `GetAbilities()` ne porte que le
#    Hero Response imprime.
#  - `sk019` Provoked! (pack three_d_man, cite par dm003/dm004) : `Faces.ReadyAll([identite], effect)` pour
#    "ready <heros>".
#
# TEXTE CONTRE CODE
#  "ready 3-D MAN" -> l'identite du joueur qui a depense la ressource (forme heros, seule forme ou le pouvoir de
#    base pourrait avoir ete incline avant de jouer une carte payee avec Tri-Power).

def GetAbilities() -> Sequence['Ability']:

    def tri_power(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse, tri_power),
    ]
