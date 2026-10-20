from . import *

# Enemies at Large — MANIGANCE ANNEXE, face A (Standard). Menace de depart 4. Permanent.
# Standard Mode Only.
# Forced Response: After the last threat is removed from here, place 1 safety counter on the main scheme
#   and 4 threat here.
# Forced Interrupt: When the last villain is defeated, reveal the top card of the villain deck and shuffle
#   the rest of its encounter set into the encounter deck. Otherwise, the players win the game.
#
# Cartes de reference :
#  - Permanent : BASE AUTOMATIQUE (`desc.Permanent`), aucun module. « Standard Mode Only » : pas de garde a
#    coder, cette face n'existe que dans data/scenarios/gs_earth_under_siege.json (standard) ; gs162b
#    (expert) porte le pendant, jamais les deux a la fois en jeu (voir gs161a).
#  - « After the last threat is removed from here, place 1 safety counter ... and N threat here » :
#    `AbilityFactory.WhenLastThreatRemoveFromThisScheme` (modele gs119 Majestrix's Verdict) ;
#    `Faces.PlaceCountersOn` sur le COMPLOT PRINCIPAL (`Worlds.FindMainScheme`), pas sur This.
#  - « When the last villain is defeated, reveal ... Otherwise, the players win the game » :
#    `AbilityFactory.WhenUnitBeDefeated(ForcedInterrupt, Villain, ...)`, condition `len(Villains.All(effect))
#    == 1` (mesuree AVANT le retrait du mechant vaincu, fait en Reponse par gs161b : voir son gabarit) ;
#    `RevelerProchainMechantEtMelangerLeReste` (earth_under_siege/__init__.py) ; victoire :
#    `Worlds.SetGameOver(True, effect)` (modele `sm/sinister_six/27102b.py`).
#
# ⚠ Mots-pieges : « the LAST villain » se juge au moment de l'INTERRUPTION (le mechant vaincu compte encore
# dans `Villains.All`) ; un deck de mechants VIDE a ce moment ne revele rien (`RevelerProchainMechantEtMelangerLeReste`
# rend None) mais le texte dit quand meme « reveal the top card » sans branche « if empty » explicite :
# lu comme « Otherwise [si aucun mechant ne reste ET le deck est vide], the players win » (le deck vide est
# la seule facon normale d'arriver a « plus aucun mechant, nulle part » une fois le dernier en jeu vaincu).


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        Unused(message)
        complot = Worlds.FindMainScheme(effect)
        if complot is not None:
            Faces.PlaceCountersOn([complot], 1, 'safety', effect)
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 4, effect)

    def dernier_mechant(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        premier = Worlds.GetFirstPlayer(effect)
        mechant = RevelerProchainMechantEtMelangerLeReste(effect, premier)
        if mechant is None:
            Worlds.SetGameOver(True, effect)

    return [
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(AbilityType.ForcedResponse, recompense),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedInterrupt,
            Villain,
            dernier_mechant,
            conditions=[lambda effect, message: len(Villains.All(effect)) == 1],
        ),
    ]
