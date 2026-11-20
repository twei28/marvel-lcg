from . import *

# Free Cassandra Nova (1B). « The players cannot win unless they help Emma Frost to escape Cassandra's control. Forced Interrupt : At the start of the player
# phase, in player order, each player not engaged with an ELITE, HELLFIRE minion reveals the top card of the Hellfire deck. If this scheme is completed, the
# players lose the game. »
# Cartes de reference : ls013 (`WhenPlayerPhaseBegin(ForcedInterrupt, op)`), 27102 Light at the End (« cannot win unless » : phrase seulement, ici Emma ne peut
# jamais etre vaincue, voir hf501a/hf501b), scheme_main.py (lit « If this scheme is completed, the players lose the game » dans le texte imprime).


def GetAbilities() -> Sequence['Ability']:
    def debut_de_phase(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        Unused(message)
        for joueur in JoueursDansLOrdre(effect):
            if not any(EstSbireEliteHellfire(m) for m in joueur.GetEngagedMinions()):
                RevelerDuDeckHellfire(effect, joueur)

    return [AbilityFactory.WhenPlayerPhaseBegin(AbilityType.ForcedInterrupt, debut_de_phase)]
