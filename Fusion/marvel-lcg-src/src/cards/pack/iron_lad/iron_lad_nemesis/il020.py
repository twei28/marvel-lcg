from . import *

# Taking Responsability — obligation nemesis d'Iron Lad (3/5)
# Forced Response: After you attack or thwart, discard the top card of
#   your deck.
# Action: Remove the top card of your deck from the game → discard this
#   obligation.
#
# Modele du declencheur : Weakened (toafk/kang/11018.py, obligation
# officielle SANS GiveTo), `AfterUnitUseBasicPower(AbilityType.ForcedResponse,
# "You", ..., powers=[...])`. Retrait du dessus du deck : meme idiome que
# il017 (GetTops + RemoveAllFromGame).
#
# CORRECTIF (trouve par verifier_tous_les_decks.py) : `Obligation.
# CheckPrintedValue` exige `desc.GiveTo` non-None sur TOUTE carte Obligation,
# meme sans texte imprime « Give to X player » (precedent officiel : 90129
# Wounded Civilians) -> `"GiveTo": "Iron Lad"` ajoute a l'entree cards.json.
# Deuxieme correctif : `.SetPlay()` sur l'action assume un `desc.Cost`
# (`assert HasCost.IsType(face)`), qu'une Obligation n'a jamais -> remplace
# par `AbilityFactory.PlayerActionToDiscardThis`, fabrique dediee "Action :
# [cout] -> defausser cette carte" sans `.SetPlay()` (modele : Weakened,
# toafk/kang/11018.py, qui l'utilise pour la meme raison).
# Troisieme correctif : `effect.GetInitiator()` peut rendre autre chose
# qu'un joueur pendant un Forced Response porte par une Obligation
# (AssertionError « self.initiator=Rhino » observe a l'usage) -> le joueur
# se lit via `message.trigger.GetControlByPlayer()` (le personnage qui a
# utilise le pouvoir de base), jamais via `effect.GetInitiator()` ici.

def GetAbilities() -> Sequence['Ability']:

    def defausse_forcee(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.trigger.GetControlByPlayer()
        Unused(this)

        joueur.DiscardDeckTopCards(1, effect)

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        initiator = effect.GetInitiator()
        Unused(message)

        Faces.RemoveAllFromGame(initiator.player_deck.GetTops(1), effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "You",
            defausse_forcee,
            powers=["ATK", "THW"],
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
            ex_operation=retirer,
        ),
    ]
