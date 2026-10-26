from . import *

# The Hellfire Conclave. Manigance annexe, 9 menaces. « Each player engaged with a HELLFIRE minion cannot thwart this scheme. Each HELLFIRE minion
# gains incite 1. When Revealed : Move 1 threat from here to the main scheme for each ELITE, HELLFIRE minion in play. »
# Cartes de reference : 27142 Guerrilla Tactics (`PlayersCannotThwartWhile`), 39035 Dial M for Mojo (`GiveKeywordToInPlayWhenApplyThis(..., incite=1)`),
# 06027 (compte des cartes en jeu). ⚠ « gains incite 1 » : le mot-cle ne se declenche que quand le sbire est REVELE pendant que la carte est en jeu.


def joueur_engage_avec_un_hellfire(effect: 'Effect', message: 'Message.CheckIfSchemeCanBeThwartBy') -> bool:
    joueur = message.by_effect.initiator
    return Player.IsType(joueur) and any(m.HasTrait("HELLFIRE") for m in joueur.GetEngagedMinions())


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        n = len([f for f in Worlds.GetOnFieldMinions(effect, CardFinder2("HELLFIRE", Minion)) if f.HasTrait("ELITE")])
        n = min(n, this.threat)
        if n > 0:
            this.RemoveThreatFromSchemes([this], n, effect)
            this.PlaceThreatOnSchemes("MainScheme", n, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("HELLFIRE", Minion), incite=1),
        AbilityFactory.PlayersCannotThwartWhile("AnyPlayer", "This", conditions=[joueur_engage_avec_un_hellfire]),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
