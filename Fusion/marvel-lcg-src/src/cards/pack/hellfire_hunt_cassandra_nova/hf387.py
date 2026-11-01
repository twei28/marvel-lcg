from . import *

# E for Extinction (TREACHERY ATTACK, x2 : hf386, hf387). Boost 1. « When Revealed : For each SENTINEL minion in play, deal 1 indirect damage to each
# player. If there is no SENTINEL minion in play, search the encounter deck and discard pile for a SENTINEL minion and put it into play engaged with you. »
# Cartes de reference : hf111 (`identity.TakeIndirectDamage(this, n, effect)`), 06027 (compte des cartes en jeu), hf381 (`MettreUneSentinelle`).
# ⚠ « each player » : chaque joueur recoit N degats indirects (qu'il repartit entre SES personnages), N = nombre de SENTINEL en jeu ; sans SENTINEL,
# seul le joueur qui revele cherche (« engaged with YOU »).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        n = NombreDeSentinelles(effect)
        if n > 0:
            for joueur in Worlds.GetPlayers(effect):
                joueur.GetIdentity().TakeIndirectDamage(this, n, effect)
        else:
            MettreUneSentinelle(effect, message.GetToPlayer())

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
