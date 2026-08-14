from . import *

# Chasing Down The Lizard (1B)

def GetAbilities() -> Sequence['Ability']:

    def derniere_menace(effect: 'Effect', message: 'Message.WhenLastThreatRemoveFromThisScheme') -> None:
        # « Forced Interrupt: When the last threat is removed from this scheme,
        # advance to stage 2A (the players win by advancing). If Curt Connors is
        # in play, remove all sanity counters from Lizard Brain, and each player
        # draws 1 card for each sanity counter removed this way. »
        this = effect.this.CastTo(MainScheme)

        connors = Worlds.FindCardOnField(effect, name="Curt Connors", card_type=Villain)
        if connors:
            cerveau = LizardBrain(effect)
            combien = CompteursDeSante(effect)
            if cerveau and combien > 0:
                Faces.RemoveCountersOn([cerveau], "All", 'sanity', effect)
                Players.ForEachPlayer(
                    effect, lambda joueur: joueur.DrawUp(combien, effect))

        this.Advance("2A", effect)

    return [
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(
            AbilityType.ForcedInterrupt,
            derniere_menace
        ),
        # « If this stage is completed, the players lose the game. »
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
