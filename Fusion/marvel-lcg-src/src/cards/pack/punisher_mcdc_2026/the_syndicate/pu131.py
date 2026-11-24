from . import *

# The Syndicate — COMPLOT ANNEXE. Menace de depart 3, Boost ★+1, 2 icones Amplify (desc `Amplify = 2`, natif).
# When Revealed : In player order, each player finds and reveals a SYNDICATE minion that is not in play.
# ★ Boost : Deal this card to yourself as a facedown encounter card.
#
# Cartes de reference : jigsaw/pu065.py (`Find.FindAndReveal` par joueur), `commun.FaceCacheeAuJoueur`
# (modele shredder / bw021).
# ⚠ « that is NOT IN PLAY » : cherche dans le deck, la defausse et les cartes de cote ; chaque joueur en revele UN,
# dans l'ordre des joueurs ; « to YOURSELF » : le joueur qui subit l'activation, pas le premier joueur.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for joueur in list(Worlds.GetPlayers(effect)):
            Find.FindAndReveal(effect, joueur, trait="SYNDICATE", card_type=Minion)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        FaceCacheeAuJoueur(effect, effect.this, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
