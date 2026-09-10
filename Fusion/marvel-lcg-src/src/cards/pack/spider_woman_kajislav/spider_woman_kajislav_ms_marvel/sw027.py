from . import *

# Fugitive — OBLIGATION de nemesis (3/5 et 4/5), x2. Boost 1.
# Give to the Julia Carpenter player.
# Forced Response: After the player phase begins, place 1 threat on Superhuman
#   Registration Act.
# Alter-Ego Action: If there is no threat on Superhuman Registration Act,
#   spend a [mental] resource -> discard Fugitive.
#
# ⚠ DEUXIEME OBLIGATION DU PACK : `sw020` Separation from the Child appartient
# au set HEROS et part avec le set nemesis A. Celle-ci est propre au set B.
# `desc.GiveTo` vaut « Julia Carpenter », le nom de l'ALTER EGO (`sw001b`) :
# c'est une base automatique (`obligation.py:42`), rien a coder pour la remise.
#
# ⚠ LA CARTE SE MORD LA QUEUE, et c'est tout son interet : elle NOURRIT l'Acte
# d'Enregistrement a chaque tour, et ne se laisse defausser que si l'Acte est
# VIDE. Il faut donc vider l'Acte, puis passer en alter ego, puis payer, avant
# que le prochain tour ne le recharge. En double dans le set.
#
# CARTES DE REFERENCE
#  - `50029` Press Conference : le patron exact d'une obligation qui reste en
#    jeu — une fenetre de phase en `ForcedResponse`, plus
#    `PlayerActionToDiscardThis(AbilityType.AlterEgoAction)`.
#  - `aa017` Funeral : le cout imprime en ressource,
#    `.SetCost(Cost("B"))` pour une [mental] (`element/resources.py:12`,
#    'b' = mental).
#
# TEXTE CONTRE CODE
#  ⚠ « After the PLAYER PHASE begins » : une fois par round, au debut de la
#    phase des joueurs, pas au debut du tour de chaque joueur.
#  ⚠ « place 1 threat on Superhuman Registration Act » : si l'Acte n'est pas
#    en jeu, rien. Le texte ne prevoit aucun repli.
#  ⚠ « If there is NO THREAT on Superhuman Registration Act » : la condition
#    porte sur la MENACE, pas sur la presence de la carte. Acte absent du jeu :
#    il n'y a effectivement aucune menace dessus, l'action est donc ouverte.
#    C'est la lecture stricte de la phrase, et le seul cas ou elle s'applique
#    est celui d'une table qui joue `sw027` sans `sw026`, que le set n'autorise
#    pas.
#  ⚠ « spend a [mental] resource » : depenser, pas defausser une carte mentale.


def GetAbilities() -> Sequence['Ability']:

    def nourrir_l_acte(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        Unused(message)
        PoserSurLActe(effect.this, 1, effect)

    def acte_vide(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        acte = ActeDEnregistrement(effect)
        return acte is None or acte.CastTo(EncounterSideScheme).threat == 0

    return [
        AbilityFactory.AfterPlayerPhaseBegin(
            AbilityType.ForcedResponse,
            nourrir_l_acte,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
            conditions=[acte_vide],
        ).SetCost(Cost("B")),
    ]
