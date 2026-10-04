from core import *
from game.card.face import *
from game.ability import *
from game.message import *
from game.player import *

class PlayerPhase:

    def __init__(self, player: 'Player') -> None:
        self.player = player

    ################################################################################
    # Phase
    def MayDiscardHandCardsAndDrawUpToMax(self, display_name: str, message: 'Message2') -> List['CardFace']:
        from game.effect.rule import GameRule
        player = self.player
        faces = player.hand_cards.Get()

        value = len(player.GetCountHandSizeFaces()) - player.hand_size
        value = value if value >= 0 else 0

        rule = GameRule(player.GetIdentity(), message, display_name=display_name)
        # AJOUT (pack custom beast) : on RETOURNE ce qui a ete ecarte. L'appel
        # etait deja fait, `AskDiscardFaces` rendait deja la liste ; seul le
        # `return` est neuf, aucun appelant existant ne le lit.
        discarded = player.AskDiscardFaces(faces, (value, "All"), rule)
        player.DrawUp("Max", rule)
        return discarded

    def ResolveMulligans(self, message: 'Message.WhenPlayerResolveMulligans') -> None:
        discarded = self.MayDiscardHandCardsAndDrawUpToMax("Resolve Mulligans", message)
        # AJOUT (pack custom beast, bt001b) : seul point du moteur ou une carte
        # peut reagir au mulligan. Voir Message.AfterPlayerResolveMulligans.
        Message.AfterPlayerResolveMulligans(self.player, discarded).Send()

    def BeginPhase(self) -> None:
        player = self.player
        player.stat.OnBeginPhase()

    def BeginTurn(self) -> None:
        player = self.player
        player.controller.manager.OnBeginTurn()
        player.stat.OnBeginTurn()
        return

    def PlayerTurn(self) -> None:
        from game.message import Message

        player = self.player
        world = player.world

        player.controller.manager.OnPlayerTurnStart()

        turn_begin_message = Message.WhenPlayerTurnBegin(player)
        turn_begin_message.Send()
        begin_message = Message.AfterPlayerTurnBegin(player, turn_begin_message)
        begin_message.Send()

        if player.is_eliminated:
            return

        message = Message.WhenPlayerInTurn(player, world.round_id)
        message.Send()
        if player.is_eliminated:
            return

        turn_end_message = Message.WhenPlayerTurnEnd(player, world.round_id)
        turn_end_message.Send()
        if player.is_eliminated:
            return
        player.res_pool.Reset()
        end_message = Message.AfterPlayerTurnEnd(player, turn_end_message)
        end_message.Send()

    def EndTurn(self):
        player = self.player
        player.stat.OnEndTurn()

    # TODO: use trigger to rewrite?
    def EndPhase(self) -> None:
        from game.card.face.card_face import CardFace
        from game.effect.rule import EndPhase
        from game.operate.faces import Faces

        player = self.player
        message = Message.WhenPlayerEndPhase(player)
        message.Send()

        # AJOUT (pack wave, 22/9/2026) : « At the end of the player phase,
        # before players draw up to their hand size, place all cards in the
        # Rising Tide area in their owner's discard pile. » Regle UNIVERSELLE
        # de la zone (comme le plafond de la Reserve, `EnforceReserveLimit`),
        # pas une capacite de carte -- appliquee a CHAQUE joueur (la zone
        # existe pour tous, `player.rising_tide`, mais ne se remplit que par
        # des effets qui la ciblent explicitement : un joueur sans carte du
        # pack `wave` y trouve toujours une zone vide, et cette purge ne fait
        # alors rien). Place AVANT `MayDiscardHandCardsAndDrawUpToMax`,
        # exactement comme l'insert l'exige.
        cartes_rising_tide = player.rising_tide.GetAll(False)
        if cartes_rising_tide:
            Faces.DiscardAll(cartes_rising_tide, EndPhase(player))

        self.MayDiscardHandCardsAndDrawUpToMax("End Phase", message)

        if player.is_eliminated:
            return

        faces: List[CardFace] = []
        effect = EndPhase(player)
        for face in player.GetControlCards():
            faces.append(face)
            for upgrade in face.GetInventoryDeck().Get():
                faces.append(upgrade)
        Faces.ReadyAll(faces, effect)

        self.player.has_change_form = False
        player.stat.OnEndPhase()

        return

    def BeginRound(self) -> None:
        player = self.player
        player.has_finished_turn_this_round = False
        player.stat.OnBeginRound()

    def EndRound(self) -> None:
        player = self.player
        player.stat.OnEndRound()

