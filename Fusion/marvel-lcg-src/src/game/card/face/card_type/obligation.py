from core import *
from game.card.face import *
from game.message import *
from game.ability import *
from game.ability.factory import *
from game.player import *
from cards.paper import Paper

# TODO:
# Only the player with the obligation in their play area
# can trigger abilities or pay costs on that obligation.

"""
If an obligation card is revealed from the encounter deck
and that obligation instructs that it must be given to a
specific player (such as “Give to the Peter Parker player”),
place that obligation into the player’s play area who controls
the associated identity. That player must decide how to
resolve the obligation.
"""

@final
# ⚠ CORRECTIF DU 08/09/2026 : `CanCrisis` AJOUTE.
# Une obligation pouvait deja porter l'icone Acceleration (`HasAccelerationIcon`,
# presente depuis toujours) et l'icone Alea (`HasHazard`), mais PAS l'icone
# Crisis : `desc.Crisis` sur une obligation faisait tomber la mise en place sur
# `KeyError: 'Crisis'` (has_attribute.py:32), donc un deck ENTIEREMENT
# injouable, et rien d'autre que `verifier_tous_les_decks.py` ne le voyait
# (lecon `ls005`). Le type `Attachment` porte les trois icones depuis toujours
# (attachment.py:7) : l'omission etait une incoherence du moteur, pas une regle.
# Trouve en portant `sm013` Future in Crisis (pack spider_man_2099, Rainy), qui
# imprime Acceleration ET Crisis sur une obligation.
# Ajout PUREMENT ADDITIF : sans `desc.Crisis`, rien ne change (printed_crisis
# vaut 0). Aucune obligation officielle n'en porte.
class Obligation(Asset2, CanHinder, HasHazard, HasAccelerationIcon, CanCrisis, HasUses, EncounterNonVillainCard, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.printed_give_to: str|None = None

        super().__init__(paper)

        self.RegisterAttribute("GiveTo", "printed_give_to", str)

    @override
    def GetAbilities(self) -> List['Ability']:
        abilities: List['Ability'] = []
        if self.paper.card_id in ["04163", "04164", "04165", "04166"]:
            def action(effect: 'Effect', message: 'Message.AfterPlayerDrewCards'):
                self.PutIntoPlay(message.GetToPlayer(), effect)

            abilities.append(
                AbilityFactory.AfterPlayerDrewCards(
                    AbilityType.Campaign,
                    "AnyPlayer",
                    self,
                    action,
                )
            )
        return abilities + super().GetAbilities()

    @override
    def CheckPrintedValue(self):
        assert self.printed_give_to != None, self.paper.card_id
        return super().CheckPrintedValue()

    @override
    def OnPlayerRevealCard(self, message: 'Message.WhenPlayerRevealCard') -> bool:
        from game.operate.worlds import Worlds
        from game.operate.faces import Faces
        from game.effect.rule import GameRule

        if self.give_to:
            found_player = Worlds.FindPlayerByName(self.give_to, message.by_effect)
        else:
            found_player = message.GetToPlayer()

        if found_player:
            message.SetGiveToPlayer(found_player)
            return super().OnPlayerRevealCard(message)
        else:
            # If the identity associated with a revealed obligation
            # card has been eliminated, ignore the card’s ability,
            # remove it from the game, and reveal an additional
            # encounter card.
            from game.operate.faces import Faces
            Faces.RemoveAllFromGame([self], GameRule(self))
            player = message.GetToPlayer()
            player.DealEncounterCards(1, GameRule(self), by_surge=True)
            return False

    @override
    def OnPutIntoPlay(self, message: 'Message.WhenCardPutIntoPlay') -> bool:
        from game.operate.faces import Faces
        Faces.MoveAllTo([self], message.GetToPlayer().obligations_area, message.by_effect)
        return super().OnPutIntoPlay(message)

    @override
    def OnWhenCardRevealed(self, revealed_message: 'Message.WhenCardRevealed') -> None:
        from game.operate.faces import Faces
        from game.effect.rule import GameRule

        found_player = revealed_message.GetGaveToPlayer()
        self.PutIntoPlay(found_player, GameRule(self))

        super().OnWhenCardRevealed(revealed_message)

        give_message = Message.WhenObligationGiveToPlayer(found_player, revealed_message)
        give_message.Send()

        if self.card.area.flags.is_dealt_encounter:
            Faces.DiscardAll([self], GameRule(self))

    ################################################################################
    #
    def GetGaveToPlayer(self) -> 'Player':
        player = self.card.area.play_area
        assert player
        return player
        # for player in World().const_players:
        #     if self in player.obligations_area.Get():
        #         return player
        # assert False, f"{self=}"

    @property
    def give_to(self) -> str:
        assert self.printed_give_to != None
        return self.printed_give_to

    @property
    @override
    def bind_face(self) -> 'Hero|AlterEgo|None':
        player = self.card.area.play_area
        if player == None:
            return None
        return player.GetIdentity()

    @override
    def GetBindFace(self) -> 'Hero|AlterEgo':
        from game.card.face.card_type import Hero
        from game.card.face.card_type import AlterEgo
        face = super().GetBindFace()
        return face.CastTo(Hero|AlterEgo)

