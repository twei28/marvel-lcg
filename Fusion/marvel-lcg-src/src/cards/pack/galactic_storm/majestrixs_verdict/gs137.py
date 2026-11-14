from . import *

# Sister's Deception — TRAITRISE (Majestrix's Verdict), 2 exemplaires. 2 icones de boost.
# When Revealed: If Lilandra is in play, she attacks you (resolve her ATK against you without exhausting her,
#   but with taking consequential damage). Otherwise, place 3 threat on Imprisoned on Chandilar.
#
# Cartes de reference :
#  - « <allie> attacks you (resolve her ATK against you without exhausting) » : modele OFFICIEL 22031 Old Rivals
#    (« If the Gamora hero or ALLY is in play, she resolves her ATK against you without exhausting ») :
#    `allie.BasicAttack([identite], effect)` ; l'attaque de base d'un allie ne l'incline pas par ce chemin et
#    applique ses degats consecutifs (`printed_attack_consequential_damage`).
#  - « Otherwise, place 3 threat on Imprisoned » : `PlaceThreatOnSchemes([prison], 3)`.
#
# ⚠ Mots-pieges : « attacks YOU » = le joueur qui revele, meme si Lilandra est controlee par un autre joueur ;
# « WITHOUT exhausting her » ; « WITH taking consequential damage » (1 degat sur Lilandra).


def GetAbilities() -> Sequence['Ability']:

    def tromperie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        lilandra = LilandraEnJeu(effect)
        if lilandra is not None:
            lilandra.BasicAttack([joueur.GetIdentity()], effect)
            return
        prison = Prison(effect)
        if prison is not None:
            effect.this.PlaceThreatOnSchemes([prison], 3, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, tromperie),
    ]
