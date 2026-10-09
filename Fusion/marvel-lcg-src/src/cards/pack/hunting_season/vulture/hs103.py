from . import *

# hs103 Ravenous Onslaught
# Alter-Ego : Vulture manigance. Heros : Vulture vous attaque. Surge si vous avez moins de la moitie de vos PV max.

def GetAbilities() -> Sequence['Ability']:

    def surge_si_blesse(effect: 'Effect', joueur: 'Player') -> None:
        if MoinsDeLaMoitie(joueur.GetIdentity()):
            ThisCardGainSurge(effect)

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        v = Vulture(effect)
        if v is not None:
            v.CastTo(Enemy).DoSchemes(joueur, effect)
        surge_si_blesse(effect, joueur)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        v = Vulture(effect)
        if v is not None:
            v.CastTo(Enemy).DoAttackYou(joueur, effect)
        surge_si_blesse(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
