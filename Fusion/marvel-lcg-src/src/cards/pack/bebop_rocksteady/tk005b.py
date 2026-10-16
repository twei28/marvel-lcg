from . import *

# Demolition Crew (1B) : « When this scheme would be completed, remove all threat
# from here instead. Then, in player order, Bebop and Rocksteady attack each player
# (even if they are in alter-ego form). » Pas de « les joueurs perdent » imprime :
# le complot boucle indefiniment.

def GetAbilities() -> Sequence['Ability']:

    def completer(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        avant = this.threat
        this.RemoveThreatFromSchemes([this], "All", effect)
        if avant > 0 and this.threat >= avant:
            return                       # menace non retiree : l'interruption ne se resout pas (ruling 32)
        message.SetBeInstead(effect)
        for joueur in Worlds.GetPlayers(effect):
            for vilain in VilainsEnJeu(effect):
                if effect.world.is_game_over:
                    return
                if vilain.IsInPlay():
                    vilain.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.WhenCompleted, "This", completer),
    ]
