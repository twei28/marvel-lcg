from . import *

# The King — ENVIRONNEMENT de campagne (combat 4, p273, 3/3 de Kingsfall). Setup. Permanent. MULTI-TABLES seulement (mis en jeu par pu147 quand la partie
# appartient a une assemblee ; en miroir chez TOUS les groupes : decision 3 de l'utilisateur, 22/10/2026).
# Forced Interrupt : When Kingpin is defeated in this pod, place 1 damage here for each player in that game.
# Forced Interrupt : When the players lose a game in this pod, place 1 threat here for each player in that game.
# At the end of all games, if the amount of damage here is equal to or greater than the amount of threat, the pod wins!
#
# Cartes de reference : challenges/2408 (`Ability(..., Message.WhenGameOver, ...)` sur la fin de partie), `game/operate/assemblee.py` (stockage commun),
# `SynchroniserLaTable` (set __init__) qui affiche les totaux communs sur le miroir.
# ⚠ Mots-pieges :
#  - les degats et la menace sont COMMUNS a l'assemblee : on les ecrit dans le stockage partage (`Assemblee.Terminer`, une seule fois par table) et le miroir
#    de chaque table les affiche (compteurs `king_damage` / `king_threat`, pas `damage` / `threat` qui ont un sens pour les ennemis et les manigances) ;
#  - « 1 per player in THAT game » : le nombre de joueurs de CE groupe ;
#  - « at the end of ALL games » : le verdict n'existe que quand toutes les tables sont finies (ou fermees : une table qui part compte comme une defaite,
#    decision 2) ; il se lit dans `Assemblee.Etat(code)['gagnee']`, et s'affiche sur l'ecran de fin.


def GetAbilities() -> Sequence['Ability']:

    def fin_de_partie(effect: 'Effect', message: 'Message.WhenGameOver') -> None:
        pod = Pod(effect)
        if pod is None:
            return
        Assemblee.Terminer(pod[0], pod[1], bool(message.players_won))
        SynchroniserLaTable(effect)

    return [
        Ability(AbilityType.ForcedInterrupt, Message.WhenGameOver, [], fin_de_partie),
    ]
