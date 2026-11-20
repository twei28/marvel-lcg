from . import *

# Portal Trouble (POTENTIAL ALLY, Blink). Victory 1.
# Forced Response: When the villain phase begins, each player discard 1 card from hand in random.
# When Defeated: le joueur qui la defait cherche Blink dans la zone mise de cote.
#
# Cartes de reference : fiche defausse-au-hasard.md (`joueur.DiscardRandomHandCards(1, effect)`, deja employe par ~40 cartes),
# `AbilityFactory.WhenVillainPhaseBegin` (turn_phase.py). « EACH player » : tous les joueurs, dans l'ordre.
def GetAbilities() -> Sequence['Ability']:
    def portail(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        for joueur in Worlds.GetPlayers(effect):
            joueur.DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedResponse, portail),
        AbilitePotentialAlly("Blink"),
    ]
