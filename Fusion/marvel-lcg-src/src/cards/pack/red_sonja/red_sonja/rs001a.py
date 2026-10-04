from . import *

# * Red Sonja — HEROS. THW 1 / ATK 2 / DEF 2, main 5, 10 PV. ADVENTURER.
# She-Devil — Action: Exhaust a WEAPON upgrade you control -> play an event
# from your hand, reducing its resource cost by 1.
#
# CARTES DE REFERENCE
#  - `an003` Heven's Fury (pack angela) : `CostFunc.Exhaust(trait="WEAPON")`
#    pour « exhaust a WEAPON upgrade/you control you control » exactement.
#  - `ar001a` Bring the War (pack ares) : « Action: ... -> play an event from
#    your hand » sur la face HEROS, choix parmi `joueur.hand_cards` filtre
#    `Event.IsType`, joue via `joueur.PlayCardsLikeInTurn(...)`.
#  - `player_action.py:937`, `PlayCardsLikeInTurn(..., update_resources_cost=-1)` :
#    reduit reellement le cout de LA carte jouee (pas « ignore », comme Ares,
#    mais « -1 »), enregistre via `ReduceCostToPlayThis(which_effect=...)`
#    en interne -- exactement « reducing its resource cost by 1 ». ⚠ Le
#    parametre attend une valeur NEGATIVE pour reduire (verifie contre tous
#    les autres appels du depot, cf. `red_sonja/__init__.py`).
#
# TEXTE CONTRE CODE
#  ⚠ « Action », pas « Hero Action » : capacite imprimee sur la face HEROS
#    elle-meme (comme `ar001a` Bring the War) -> `AbilityType.Action`.
#  ⚠ « a WEAPON upgrade you control » : `CostFunc.Exhaust(trait="WEAPON")`,
#    pas de nom precis, choix du joueur parmi les siennes.
#  ⚠ « play an event from your hand » : filtre `Event.IsType`, PAS n'importe
#    quelle carte (`ar001a` filtre pareil).
#  ⚠ « reducing its resource cost by 1 » : `update_resources_cost=1`, pas
#    `ignore_resources_cost` (qui annulerait tout le cout).
#
# rs006/rs007/rs008 lisent chacun `AUtiliseSheDevil(this)` (`__init__.py` de
# ce dossier) pour savoir si LEUR PROPRE mise en jeu vient de cette Action.
#
# ⚠⚠ SECONDE CAPACITE POSEE ICI, PAS SUR rs009 (23/09/2026, bug trouve par
# le cas de test de rs009) : « While Queen of Sogaria is in the victory
# display, Red Sonja gains: Response: After you exhaust Hyrkanium Blade,
# draw 1 card. (Limit once per round.) » -- voir `QueenDeSogariaEstEnVitrine`
# (`__init__.py` de ce dossier) pour le detail complet du piege (une carte
# dans la vitrine est hors jeu, ses propres capacites ne sont jamais
# enregistrees). Postee sur l'IDENTITE, qui reste toujours en jeu, avec la
# vitrine relue comme simple CONDITION externe a chaque exhaustion
# d'Hyrkanium Blade.

def GetAbilities() -> Sequence['Ability']:

    def she_devil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player):
            return
        JouerEvenementReduitParSheDevil(effect, joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            she_devil,
        ).SetName("She-Devil")
        .SetCostFunc(CostFunc.Exhaust(trait="WEAPON")),
        CapaciteQueenDeSogariaEnVitrine(),
    ]
