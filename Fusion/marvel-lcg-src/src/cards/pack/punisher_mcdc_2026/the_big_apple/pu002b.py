from . import *

# Silence the City (2B) — MANIGANCE PRINCIPALE. Menace 8 par joueur, depart 2 par joueur, acceleration +1 par joueur.
# Forced Interrupt : When a villain would be defeated, instead reset their hit points and place 1 quell counter on them.
# Forced Response : After the end of the player phase, if each villain has at least 1 quell counter, advance to stage 3A
#   (the players win by advancing).
# If this scheme is completed, the players lose the game.
#
# Cartes de reference : pu001b (meme interruption), fne/typhoid_mary (`SetBeInstead`, `ResetHealth`), `AfterPhaseEnd(ForcedResponse, "Player", ...)`
# (skrull_menace/secret_invasion), compteur maison 'quell' (CardFace.COUNTER).
# ⚠ « each villain » : TOUS les CAPO en jeu (au moins un, sinon rien a avancer) ; un CAPO peut etre vaincu plusieurs fois (le compteur s'ajoute,
# la condition reste « au moins 1 ») ; « after the END of the player phase » : fin de la phase des joueurs, pas du round.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        message.SetBeInstead(effect)
        villain = message.trigger
        villain.ResetHealth(effect)
        Faces.PlaceCountersOn([villain], 1, 'quell', effect)

    def chacun_a_un_quell(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> bool:
        mechants = list(Worlds.GetAllVillains(effect))
        return bool(mechants) and all(v.GetCounters('quell') >= 1 for v in mechants)

    def avancer(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        effect.this.CastTo(MainScheme).Advance(None, effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, Villain, vaincu),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Player", avancer, conditions=[chacun_a_un_quell]),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
