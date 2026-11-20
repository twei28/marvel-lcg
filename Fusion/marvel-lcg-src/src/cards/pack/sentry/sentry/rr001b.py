from . import *

# * Robert Reynolds (face ALTER-EGO) : CIVILIAN. REC 4, main 5, PV 16.
# Setup: Put your Duality Aspect upgrade into play with 0 balance counters on it. (See insert.)
# Response: After you change to this form, you may remove up to 2 balance counters from play.
#
# CARTES DE REFERENCE
#  - Setup : Duality Aspect porte `desc.Permanent` (donnees) : le moteur la met en jeu a la mise en place, SANS compteur : aucun code ici (fiche `permanent.md`, `setup.md`).
#  - « After you change to this form » : `AbilityFactory.AfterFlipToThisFace(Response, op)` (modele `wn001a`, `ch001b`).
#
# TEXTE CONTRE CODE
#  « you MAY remove » : la Reponse est facultative (type `Response`). « UP TO 2 » : on retire autant que possible, jusqu'a 2 ; l'ordre est d'abord Duality Aspect puis les autres
#  cartes (The Watchtower) : le texte dit « from play », sans imposer la carte. Pas de limite au nombre de compteurs en jeu (insert).
#  Chiffres : PV 16, main 5, REC 4.


def GetAbilities() -> Sequence['Ability']:

    def retirer_deux(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        Unused(message)
        RetirerEquilibre(effect, 2)

    return [
        AbilityFactory.AfterFlipToThisFace(
            AbilityType.Response,
            retirer_deux,
        ).SetName("Duality"),
    ]
