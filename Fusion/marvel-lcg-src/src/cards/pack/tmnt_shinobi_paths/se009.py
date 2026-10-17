from . import *

# Ashigaru — PATH hybride (avance), classes Bushido + Taijutsu (Inkwire, TMNT Shinobi). BUSHIDO. TAIJUTSU.
# Permanent. You get -1 hand size. You gain the SOLDIER trait.
# Light of Foot — Hero Resource: Exhaust this card -> generate a [wild] resource. If you paid for a Shinobi
#   card with this resource, draw 1 card.
#
# Mots-cles (fiches lues AVANT le code) : Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « Hero Resource: Exhaust this card -> generate a [wild] resource » : `jennika/tj009` Tekko-Kagi
#    (`CanGenerateResources(HeroResource, Resources("G"), ...)` + `CostFunc.Exhaust("This")`), ici SANS
#    restriction de carte payee (la ressource paie TOUT) ;
#  - « if you paid for X with this resource » : `ex_operation` de `CanGenerateResources` -> rappel apres chaque
#    generation, avec `message.paying_card` (la carte payee) ; `Message.WhenPlayerPayingResources`.
#
# TEXTE CONTRE CODE
#  ⚠ « generate a [wild] resource » : UNE ressource wild (icone imprimee « etoile » : a verifier au scan contre
#    une carte du pack, voir .planning/tmnt/shinobi-socle-questions.md Q-S4) ; « Hero Resource » : forme heros.
#  ⚠ « If you paid for a SHINOBI card WITH THIS RESOURCE » : seulement quand la ressource de CETTE Voie sert
#    a payer l'entree en jeu d'une carte Shinobi (Dual comprise) ; payer une carte non Shinobi avec elle ne pioche
#    rien ; une Shinobi payee par d'autres ressources non plus.
#  ⚠ « draw 1 card » : UNE carte, a chaque paiement concerne (la ressource n'est generee qu'une fois par
#    redressement : le cout incline la Voie).


def GetAbilities() -> Sequence['Ability']:

    def lumiere_du_pied(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Path)
        Unused(this)
        paye = message.paying_card
        if paye is None or not EstShinobi(paye):
            return
        if not getattr(message.for_effect.ability, "is_play", False):
            return
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1, trait="SOLDIER"),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            ex_operation=lumiere_du_pied,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
