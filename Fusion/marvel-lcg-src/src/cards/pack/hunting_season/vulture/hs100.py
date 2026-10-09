from . import *

# hs100 Sweeping Swoop
# When Revealed : etourdissez votre identite, defaussez une carte de la main, surge si vous avez AERIAL.
# Boost : si le personnage qui active a AERIAL, une carte boost supplementaire.

def GetAbilities() -> Sequence['Ability']:

    def faucher(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        Faces.GiveStatus([identite], "Stunned", effect)
        DefausserUneCarteDeLaMain(effect, joueur)
        if identite.HasTrait("AERIAL"):
            ThisCardGainSurge(effect)

    def en_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if message.activating_enemy is not None and message.activating_enemy.HasTrait("AERIAL"):
            message.GiveActivatingEnemyAdditionalBoostCard(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, faucher),
        AbilityFactory.WhenCardBecomeBoost("This", en_boost),
    ]
