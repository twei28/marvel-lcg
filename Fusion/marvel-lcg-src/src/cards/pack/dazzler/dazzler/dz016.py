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
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            effacer,
            conditions=[
                # Sans chanson marquee, l'option ne doit pas etre offerte :
                # elle ne changerait rien et le pilote la reprendrait en
                # boucle (piege wd165).
                lambda effect, message: len(SongsAvecCompteur(effect)) > 0,
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
