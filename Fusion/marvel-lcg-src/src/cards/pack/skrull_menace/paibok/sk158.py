from . import *

# Council Manipulation — TRAITRISE (Paibok). 1 boost.
# When Revealed: Paibok schemes. If you are stunned or confused, this card gains surge.
#
# Cartes de reference :
#  - Le mechant manigance contre le joueur : **`sk098`** Impostor (« the villain schemes », meme coffret) /
#    `Enemy.DoSchemes(player, effect)` (enemy.py:46) ; **`01106`** Stampede pour le mechant cherche par
#    nom + type (`Worlds.FindCardOnField(name=..., card_type=Villain)`).
#  - Surge conditionnel : helper `ThisCardGainSurge(effect)` (modele `sk103`).
#
# ⚠ Mots-pieges : « IF YOU are stunned or confused » = l'identite du joueur qui REVELE (Sonne ou
# Desoriente, l'un OU l'autre) ; « PAIBOK schemes » : le MECHANT, pas le sbire nemesis de Lyja du meme nom ;
# l'ordre imprime est « schemes, then surge ».


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        paibok = PaibokEnJeu(effect)
        if paibok is not None:
            paibok.DoSchemes(joueur, effect)
        identite = joueur.GetIdentity()
        if identite.IsStunned() or identite.IsConfused():
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
