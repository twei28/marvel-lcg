from . import *

# Enemies at Large — MANIGANCE ANNEXE, face B (Expert). Menace de depart 5. Permanent.
# Expert Mode Only.
# Forced Response: After the last threat is removed from here, place 1 safety counter on the main scheme
#   and 5 threat here.
# Forced Interrupt: When the last villain is defeated, reveal the top card of the villain deck and shuffle
#   the rest of its encounter set into the encounter deck. Otherwise, the players win the game.
#
# Identique a gs162a (Standard), seul le nombre de menace change (5 au lieu de 4, depart et Reponse
# forcee) : voir son gabarit pour les cartes de reference et les mots-pieges.


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        Unused(message)
        complot = Worlds.FindMainScheme(effect)
        if complot is not None:
            Faces.PlaceCountersOn([complot], 1, 'safety', effect)
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 5, effect)

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
