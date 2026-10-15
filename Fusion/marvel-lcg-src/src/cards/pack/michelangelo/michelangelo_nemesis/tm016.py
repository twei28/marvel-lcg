from . import *

# Smash! — traitrise nemesis, x3 (3/5, 4/5, 5/5). Boost 2.
# When Revealed: You take 2 indirect damage.
#
# Cartes de reference :
#  - `rainy/thor_jane_foster_nemesis/ra027` : degats indirects poses sur
#    l'identite, la repartition est geree par le moteur —
#    `player.GetIdentity().TakeIndirectDamage(this, n, effect)`
#    (can_health.py:185, `AssignDamage` sur identite + allies) ;
#  - revelation d'une traitrise : `message.GetToPlayer()`.
#
# ⚠ Mots-pieges :
#  - « YOU take » : le joueur a qui la carte est revelee.
#  - « 2 INDIRECT damage » : repartis librement entre identite et allies (pas
#    de Robuste applique d'office a l'identite seule).

def GetAbilities() -> Sequence['Ability']:

    def smash(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            smash,
        ),
    ]
