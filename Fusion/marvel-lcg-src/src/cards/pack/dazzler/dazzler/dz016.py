from . import *

# Sound Collector Suit
# ARMOR. ITEM.
# Dazzler gets +1 DEF.
# Resource: Exhaust Sound Collector Suit -> generate a [energy] resource for a
#   SONG or remove 1 sound counter from a SONG in the Setlist.
#
# La carte offre DEUX usages pour un meme epuisement. Le moteur interdit deux
# `CanGenerateResources` sur une meme carte (assert de card_player.py, piege
# paye sur Jet Belt 58008), mais ici le second usage n'est PAS une generation
# de ressource : c'est une action. On les separe donc proprement.
#
#   - la ressource, bornee au paiement d'un [[SONG]] (modele Jet Belt, qui lit
#     `message.paying_for_effect.this` pour savoir ce qu'on paie) ;
#   - une action d'epuisement qui efface une marque `sound`, la SEULE carte du
#     pack capable de rendre une chanson a nouveau repetable.


def GetAbilities() -> Sequence['Ability']:

    def paie_une_chanson(effect: 'Effect',
                         message: 'Message.CheckPlayerCanPayCost') -> bool:
        paye = message.paying_for_effect.this
        return paye is not None and paye.HasTrait(TRAIT_SONG)

    def effacer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        marquees = SongsAvecCompteur(effect)
        if not marquees:
            return
        chanson = joueur.AskChooseOneText(marquees) if len(marquees) > 1 \
            else marquees[0]
        if chanson is not None:
            EffacerRepete(effect, chanson)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            defense=1,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("Y"),
            conditions=[paie_une_chanson],
        ).SetCostFunc(CostFunc.Exhaust("This")),
        # « ... OR remove 1 sound counter from a SONG in the Setlist » : branche
        # de la capacite RESOURCE, donc jouable SEULEMENT PENDANT UN PAIEMENT
        # (decision de l'utilisateur, Q2 du backlog 12, 20/10/2026, Rules
        # Reference v1.8 RESOURCE ABILITY). Le moteur n'admet qu'UNE
        # `CanGenerateResources` par carte et exige qu'une ressource generee
        # vaille au moins 1 (`assert res.val > 0`, resources.py) : une branche
        # « sans ressource » n'y est pas exprimable. ECART ASSUME : la fenetre
        # est la Reponse au message de paiement `AfterCardsBeSpendAsResource`
        # (des cartes viennent d'etre depensees pour payer une carte du
        # joueur). Consequences : la fenetre n'existe que si au moins une
        # ressource a ete depensee (une carte a cout 0 ne l'ouvre pas), et elle
        # arrive juste APRES la depense plutot qu'au choix des moyens de
        # paiement. La combinaison s'incline : elle ne peut plus produire
        # d'energie, ce qui garde le « au lieu de » de la carte.
        Ability(
            AbilityType.Response,
            Message.AfterCardsBeSpendAsResource,
            [
                lambda effect, message:
                    effect.this.IsInPlay() and
                    message.GetToPlayer() == effect.this.GetControlBy() and
                    effect.this not in (message.faces or []),
                lambda effect, message: len(SongsAvecCompteur(effect)) > 0,
            ],
            effacer,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
