from . import *

# Swarm Superiority — ATTACHEMENT (Baxter's Lab 6/22, x2). CONDITION. 1 boost.
# Attach to a SWARM minion. If you cannot, this card gains surge.
# Attached minion gains AERIAL and guard.
# When Revealed: Place 2 all-purpose counters on attached minion.
#
# Cartes de reference : `sk177` / `sk251` (`AttachToFaceWhenPutIntoPlay(Minion, ...,
# if_cannot_gain_surge=True)`) ; `GiveKeywordToAttached(..., trait=, guard=)` (RECETTES §3, 05023) ;
# `gmw/16034` pour « all-purpose counter » (le compteur est celui de la carte qui le porte, helper
# `PlacerUnCompteurSur`).
#
# Mots-pieges : « a SWARM minion » (le TRAIT, pas un nom ; y compris les sbires SWARM de Donatello) ;
# « If you CANNOT » (aucun sbire SWARM en jeu : surge) ; « attached minion gains AERIAL AND guard » (le
# trait ET le mot-cle, tant que la carte est attachee) ; « 2 counters on ATTACHED minion » (pas sur la carte).


def GetAbilities() -> Sequence['Ability']:

    def deux_compteurs(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        sbire = this.attached_face
        if sbire is not None:
            PlacerUnCompteurSur(sbire, 2, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(trait=TRAIT_SWARM, card_type=Minion),
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(Minion, trait="AERIAL", guard=1),
        AbilityFactory.WhenThisRevealed(None, deux_compteurs),
    ]
