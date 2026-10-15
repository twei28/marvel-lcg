from . import *

# Going Nova — TRAITRISE x2 (Skrull Elite - Xavin). 3 icones de boost.
# When Revealed: Assign 2[per_hero] indirect damage among players.
#
# Cartes de reference :
#  - « Assign N indirect damage among players » : **`sk163`** Asti the All-Seeing / **`gmw 16085b`** Museum Ship
#    (`premier.AssignDamage(unites, this, degats, effect)`, le premier joueur repartit entre les personnages de
#    tous les joueurs) ; **`jj020`** (meme appel, le joueur qui revele).
#  - 2[per_hero] : `Worlds.ConvertPerPlayerIconToInt("2*", effect)` (worlds.py).
#
# ⚠ Mots-pieges : « INDIRECT » (repartis par un joueur entre les personnages, pas infliges a l'identite) ; « among
# PLAYERS » (tous les personnages de tous les joueurs, repartis par le premier joueur : meme lecture que sk163) ;
# « 2[per_hero] » : 2 x le nombre de joueurs (2, 4, 6), jamais 2 fixe.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        Unused(message)
        degats = Worlds.ConvertPerPlayerIconToInt("2*", effect)
        premier = Worlds.GetFirstPlayer(effect)
        unites = [u for joueur in Worlds.GetPlayers(effect) for u in joueur.GetControlCharacters()]
        if degats > 0 and unites:
            premier.AssignDamage(unites, this, degats, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
