from . import *

# Jailbreak at the Hellfire Club (1B). « Threat cannot be removed from this scheme. Forced Interrupt : When Sebastian Shaw would scheme against
# you, deal you 1 facedown encounter card instead. If this stage is completed, the players lose the game. » (le dernier est lu dans le texte imprime).
# Cartes de reference : 01139b Countdown to Oblivion (`ThreatCannotBeRemovedFromWhile("This")`), sk099 (`WhenUnitWouldScheme` + `SetBeInstead`),
# 40146 / the_hunger_core (« instead » d'une activation).


def GetAbilities() -> Sequence['Ability']:
    def au_lieu_de_comploter(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        joueur = message.against_player
        if joueur is not None:
            joueur.DealEncounterCards(1, effect)
        message.SetBeInstead(effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile("This"),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, SurShaw(), au_lieu_de_comploter),
    ]
