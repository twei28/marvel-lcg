from . import *

# S.H.I.E.L.D. Support Team — AMELIORATION de campagne (recompense du combat 3, p268). Permanent.
# Forced Response : After this card enters play, place 1 intelligence counter here, plus 1 more for each player who did not play the last game together.
# Response : After a player defeats a minion, remove 1 counter from here -> each player draws 1 card. Deal 1 player an encounter card.
#
# Cartes de reference : pu141 / pu143 (meme compte « joueurs absents de la partie precedente » : `JetonsDeDepart`), wolv/35015 (`AfterUnitAttackAndDefeatUnit`
# + cout), `AbilityFactory.AfterCardEnterPlay(ForcedResponse, "This", ...)`, `player.DrawUp`/`DealEncounterCards`.
# ⚠ Mots-pieges :
#  - « After this card ENTERS PLAY » (et non « Setup ») : en jeu au combat 3 elle arrive par le retournement de pu144, donc EN COURS de partie ;
#  - « After a PLAYER defeats a minion » : `Friend` (identite ou allie), un sbire (pas un vilain) ; la chaine "Players" est refusee par `CheckWhichCard` ; pas « attacks and defeats » :
#    toute defaite par un joueur ; le Punisher (pu146) n'est pas un joueur ;
#  - « remove 1 counter -> » : le retrait est le COUT ; sans compteur, la Reponse n'est pas offerte ;
#  - « each player draws 1 card. Deal 1 player an encounter card » : TOUS les joueurs piochent, puis UN joueur (au choix du premier joueur, la RR ne dit
#    pas qui choisit) recoit une carte de rencontre face cachee.

def GetAbilities() -> Sequence['Ability']:

    def en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        Faces.PlaceCountersOn([effect.this], JetonsDeDepart(effect), 'intelligence', effect)

    def renseignement(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        Unused(message)
        joueurs = TousLesJoueurs(effect)
        for joueur in joueurs:
            joueur.DrawUp(1, effect)
        premier = Worlds.GetFirstPlayer(effect)
        cible = premier.AskChooseOneText(joueurs) if len(joueurs) > 1 else joueurs[0]
        if cible is not None:
            cible.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, "This", en_jeu),
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.Response, Friend, Minion, renseignement)
        .SetCostFunc(CostFunc.Counter("This", 1, 'intelligence')),
    ]
