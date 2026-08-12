from . import *

# Sleeper Agent — custom « Rainy » (obligation d'Agent 13 / Sharon Carter)
# Give to the Sharon Carter player.
# You may flip to alter-ego form. Choose:
# - Remove the Captain America ally from the game → remove Sleeper Agent from
#   the game.
# - Discard 1 card from hand and place 2 threat on the main scheme. Discard
#   this obligation.
#
# Modele : Care for Cassie (ant/ant_man/12025.py), meme charpente exacte
# (obligation « Give to X player », `YouMayFlipToYourAlterEgoForm`, puis
# `player.ChooseAbilities` entre deux options dont l'une defausse 1 carte de
# la main via `.SetTarget(from_where=["YourHandCards"], canbe_discard=True)`).
# La premiere option de Sleeper Agent ne cible pas une carte choisie par le
# joueur mais l'allie Captain America NOMME (ag002 de ce meme pack) : comme
# la premiere option de Spread Too Thin (agent_anti_venom/agent_anti_venom/
# av012.py), elle se resout sans cible via `.SetHasNoTargetEffect()`. Retirer
# du jeu passe par `Faces.RemoveAllFromGame(faces, effect)`
# (game/operate/faces.py:137), qui EST `Faces.MoveAllTo(faces,
# by_effect.world.area_removed, by_effect)` (ligne 139) enveloppee d'un
# message -- meme fonction que celle citee par le brief.
#
# Brief : « La premiere option ne doit etre proposee que si cet allie est en
# jeu. » CORRECTIF (7/8/2026, apres relecture) : la premiere version cherchait
# par nom sans filtre de controleur (`Worlds.FindCardOnField`, comme Batroc
# 50096 cherche Mysterio), ce qui rend a deux joueurs jouant tous deux
# Agent 13 le PREMIER Captain America trouve dans l'ordre du champ, peut-etre
# celui de l'autre joueur -- `CardFinder` n'expose aucun parametre de
# controleur utilisable (celui de `checker.py`/`finder.py` est commente,
# desactive). Corrige avec le meme patron qu'Assassination Plot (ag011, ce
# meme pack) : `Worlds.FindCardsOnField` (au pluriel) puis filtre manuel sur
# `GetControlByPlayer() == player` -- le joueur qui RECOIT l'obligation, pas
# n'importe quel joueur. Absent (ou controle par un autre joueur), l'option
# disparait du menu (`condition=captain_america is not None`) : le joueur
# n'a alors plus que la seconde option, comme un « Choose » a une seule
# branche legale.

def GetAbilities() -> Sequence['Ability']:

    def sleeper_agent(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        captain_americas = [
            x for x in Worlds.FindCardsOnField(effect, name="Captain America", card_type=Ally)
            if x.GetControlByPlayer() == player
        ]
        captain_america = captain_americas[0] if captain_americas else None

        def retirer_captain_america(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            if captain_america:
                Faces.RemoveAllFromGame([captain_america], effect)
            Faces.RemoveAllFromGame([this], effect)

        def defausser_et_menacer(targets: Sequence['CardFace']) -> None:
            Faces.DiscardAll(targets, effect)
            this.PlaceThreatOnSchemes("MainScheme", 2, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove the Captain America ally from the game → remove Sleeper Agent from the game",
                retirer_captain_america,
                condition=captain_america is not None,
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card from hand and place 2 threat on the main scheme. Discard this obligation",
                defausser_et_menacer,
            ).SetTarget(from_where=["YourHandCards"], canbe_discard=True),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            sleeper_agent
        ),
    ]
