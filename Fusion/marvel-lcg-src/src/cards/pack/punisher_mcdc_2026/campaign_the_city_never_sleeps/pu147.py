from . import *

# Long Live the King? — ENVIRONNEMENT de campagne (combat 4, p269, face 1A de Kingsfall). Setup. Permanent.
# Battle Setup : Scenario Kingpin ; sets SWAT Team et Tracksuit Mafia (donnees : scenario `kingsfall`) ; pods / The King : MODE MULTI-TABLES, pas ici.
# Setup : Put the Punisher ally into play under a player's control. Flip this card and place 1 counter on it.
#
# Cartes de reference : pu141 (`AfterGameSetup` : le Setup d'une carte hors scenario) et `MettreLesRecompenses` (`campaign.py` : mise en jeu sous le controle
# du premier joueur d'apres le carnet), pu144 (`RetournerPunishment` : recto-verso de types differents = echange de cartes).
# ⚠ Mots-pieges :
#  - « Put the Punisher ally into play » : SEULEMENT si le carnet dit que l'allie est gagne (`Punisher Ally` = 1, instructions de campagne : « ne mettez pas en jeu
#    l'allie Punisher si vous n'avez pas gagne le scenario precedent ») ; sans carnet, pas d'allie ;
#  - « under a player's control » : les JOUEURS choisissent (decision de l'utilisateur, 22/10/2026) : le premier joueur designe qui prend l'allie (automatique si un seul joueur) ;
#  - « Flip this card and place 1 counter on it » : le verso (6135B) est l'amelioration Power to the People (pu148), d'un autre type : on retire pu147 et on met
#    pu148 en jeu, sous le controle du premier joueur, avec 1 jeton `counter` ; ce « flip » se fait TOUJOURS, allie ou non.

def GetAbilities() -> Sequence['Ability']:
    from game.card.factory import CardFactory

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Unused(message)
        SoignerParRec(effect)     # AVANT de sortir du jeu : la 2e capacite d'une carte retiree ne partirait pas
        premier = Worlds.GetFirstPlayer(effect)
        # Le scenario Kingpin (FNE) ecrit deja son releve ; pu147 n'y ajoute que l'estampille `kingsfall` (l'id du combat 4 dans `data/campagnes/`), sans cle.
        EnregistrerLeReleve(effect, lambda e, m: {}, 'kingsfall')
        if CampaignLog.GetStrInternal(CLE_ALLIE_PUNISHER, effect) == '1':
            allie = CardFactory.GenerateCard(ALLIE_PUNISHER, None, effect.world)
            joueurs = TousLesJoueurs(effect)
            controleur = premier.AskChooseOneText(joueurs) if len(joueurs) > 1 else premier
            allie.face.PutIntoPlay(controleur or premier, effect, under_control=True)
        Faces.RemoveAllFromGame([effect.this], effect)
        pouvoir = CardFactory.GenerateCard(POUVOIR_AU_PEUPLE, None, effect.world)
        pouvoir.face.PutIntoPlay(premier, effect, under_control=True)
        Faces.PlaceCountersOn([pouvoir.face], 1, 'counter', effect)

    return [
        AbilityFactory.AfterGameSetup(mise_en_place),
    ]
