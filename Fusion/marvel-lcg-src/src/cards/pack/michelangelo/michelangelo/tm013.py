from . import *

# All Alone — obligation. Boost 2. Give to the Mikey player.
# Flip to alter-ego form. Exhaust each ally and support you control. You cannot
#   change forms.
# Alter-Ego Action: Exhaust your identity and discard 1 card from your hand ->
#   remove All Alone from the game.
#
# Cartes de reference :
#  - `storm/36030` Claustrophobia (« Flip to alter-ego form. You cannot change
#    forms. Alter-Ego Action: ... remove from the game ») : `WhenThisRevealed(
#    None, op)` + `PlayersCannotChangeForms(NonKeyword, "AttachedPlayer")` +
#    `PlayerActionToRemoveThisFromGame(AlterEgoAction)` ;
#  - cout a deux parties (epuiser l'identite ET defausser 1 carte) :
#    `sunfire/sf010` Shame — deux `SetCostFunc` chaines ;
#  - epuiser allies et soutiens : `Faces.ExhaustAll(faces, effect)` ;
#    `player.GetControlCardsByType(ally=True, support=True)` (50029).
#
# ⚠ Mots-pieges :
#  - « Exhaust EACH ally AND support YOU control » : les deux types, ceux du
#    joueur donne seulement.
#  - Les trois premieres phrases ne s'appliquent qu'a la REVELATION ; « You
#    cannot change forms » dure TANT QUE la carte est en jeu.
#  - « remove All Alone from the game » : retrait de la partie, PAS defausse
#    (PlayerActionToRemoveThisFromGame).
#  - Le « → » regroupe DEUX couts : les deux sont obligatoires ensemble.
#  - desc.GiveTo = « Mikey » (nom de l'alter-ego), pas « Michelangelo ».

def GetAbilities() -> Sequence['Ability']:

    def all_alone(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = this.GetGaveToPlayer()
        if joueur is None:
            return

        identite = joueur.GetIdentity()
        if identite is not None:
            identite.ChangeToForm(AlterEgo, effect)

        faces = joueur.GetControlCardsByType(ally=True, support=True)
        if faces:
            Faces.ExhaustAll(faces, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            all_alone,
        ),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AttachedPlayer",
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
