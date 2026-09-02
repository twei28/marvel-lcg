from . import *

# Grounded — OBLIGATION. Boost 2 (deux icones rouges lues sur le scan).
# Give to the Viv Vision player.
# Flip to alter-ego form.
# You cannot change form.
# Alter-Ego Action: Exhaust your alter-ego -> remove Grounded from the game.
#
# Carte de reference : 36030 Claustrophobia (obligation de Storm),
# src/cards/pack/storm/storm/36030.py. C'est le MEME TEXTE, mot pour mot, aux
# noms propres pres :
#   « Flip to alter-ego form. You cannot change forms.
#     Alter-Ego Action: Exhaust Ororo Munroe -> remove Claustrophobia from the
#     game. »
# Les trois fabriques employees la-bas rendent exactement les trois phrases
# imprimees ici, et ce module en est la transposition directe :
#   - `WhenThisRevealed(None, ...)` + `identity.ChangeToForm(AlterEgo, effect)`
#   - `PlayersCannotChangeForms(AbilityType.NonKeyword, "AttachedPlayer")`
#   - `PlayerActionToRemoveThisFromGame(AbilityType.AlterEgoAction)
#      .SetCostFunc(CostFunc.Exhaust("YourIdentity"))`
#
# ⚠ NE PAS partir de 12025 Care for Cassie, bien qu'elle porte aussi
# « cannot change form » : elle imprime « You MAY flip » et un choix a deux
# branches, deux differences de fond. Grounded n'offre aucun choix.
#
# ⚠ `desc.GiveTo` = « Viv Vision », le nom de l'ALTER-EGO (PROCESSUS-HEROS
# etape 1). Les deux faces de Viv portent le meme nom, la resolution est donc
# sans ambiguite : `Worlds.FindPlayerByName` passe par
# `identity.IsName(name, check_all_face=True)` (player.py:262), qui ignore
# l'etoile d'unicite — meme mecanique que « Scott Lang » pour 12025.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « FLIP to alter-ego form » sans « you may » : la bascule est
#    OBLIGATOIRE. `ChangeToForm(AlterEgo, effect)` ne fait rien si le joueur
#    est deja en alter-ego, ce qui est le comportement correct.
#  - « You cannot change FORM » (singulier ici, pluriel sur Claustrophobia) :
#    aucune difference de sens, l'interdiction porte sur les deux sens.
#  - L'interdiction est PERMANENTE tant que l'obligation est en jeu, et non
#    « until your next turn ends » comme 12025 : c'est `PlayersCannotChangeForms`
#    (continu), pas `Players.CannotChangeFormDuringNextTurn`.
#  - « Exhaust YOUR ALTER-EGO » : l'identite, donc `CostFunc.Exhaust(
#    "YourIdentity")`, et l'`AlterEgoAction` garantit qu'on est bien sur la
#    face civile.
#  - « REMOVE ... FROM THE GAME », pas « discard » : l'obligation ne revient
#    jamais dans le deck rencontre. `PlayerActionToRemoveThisFromGame`.
#  - L'obligation ne convoque personne : le pack n'a aucune carte nemesis, et
#    c'est le modulaire Zzzax qui remplit `nemesis_set` (voir le __init__ du
#    pack). Ne pas chercher de sbire a reveler ici.
#  - HOMONYMES : « Grounded » est aussi une obligation de Jubilee (47023) et
#    un environnement d'Electro (wd041). Sets differents, aucun risque.


def GetAbilities() -> Sequence['Ability']:

    def grounded(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)

        joueur = this.GetGaveToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        identite.ChangeToForm(AlterEgo, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            grounded,
        ),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AttachedPlayer",
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
