from . import *

# Sound Absorption
# RESOURCE. (2 x [energy])
# Response: After you spend this card, place 2 sound counters on your identity.
#
# CONSEQUENCE D'UN CHOIX DE VERSION, assume par l'utilisateur le 29/08/2026.
# Le pack livre DEUX versions de la carte heros :
#   - celle du dossier `Hero`, retenue ici : « Rehearsal — Hero Action: PLACE
#     1 sound counter on a SONG in the Setlist » ; le compteur nait sur la
#     chanson, il ne vient de nulle part ;
#   - celle de la fiche de regles `Insert.png` : « Sound to Light — Response:
#     After resolving a SONG event, place 1 sound counter on Dazzler (max 4) »
#     puis « Spotlight — Hero Action: MOVE 1 sound counter from Dazzler to a
#     SONG ». La, l'identite est le RESERVOIR, et cette carte le remplit.
# L'utilisateur a choisi la version imprimee sur la carte. Les compteurs poses
# ici sur l'identite n'ont donc aucun consommateur : on rend la carte a la
# lettre, les compteurs sont bien poses et visibles, mais rien ne les depense.
# Idem pour « Love from Beyond the Stars » (dz038).
#
# L'identite, elle, herite bien de `CanPlaceCounter` : contrairement aux
# evenements, elle sait porter des compteurs.


def GetAbilities() -> Sequence['Ability']:

    def absorption(effect: 'Effect',
                   message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.PlaceCountersInternal(2, COMPTEUR, effect)

    return [
        # `AfterYouSpendThisCard` porte deja `NoOutOfPlayLimit` : la carte est
        # a la defausse au moment ou la reponse se declenche.
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            absorption,
        ),
    ]
