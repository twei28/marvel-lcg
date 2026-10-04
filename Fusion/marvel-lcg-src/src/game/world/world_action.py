from core import *
from game.card.face import *
from game.effect import *
from game.player import *
from game.world import *
from game.world.game_area import *

class WorldAction:
    from game.card.face.card_type import Ally
    from game.card.face.card_type import Minion
    from game.card.face.base import Villain
    Character = AlterEgo|Hero|Ally|Villain|Minion

    def GetWorld(self) -> 'World':
        from game.world import World
        return Cast(World, self)

    ################################################################################
    # Player
    @property
    # Use `ForEachPlayer(effect)` when using this to implement ability
    def const_players(self) -> List['Player']:
        world = self.GetWorld()
        return world.players[:]

    def GetFirstPlayer(self) -> 'Player':
        world = self.GetWorld()
        for player in world.players:
            if not player.is_eliminated:
                return player
        # return self.GetWorld().players[0]
        assert False
    def GetCurrentPlayer(self) -> 'Player':
        world = self.GetWorld()
        if world.asking_player:
            return world.asking_player[-1]
        elif world.is_game_started and \
            world.phase.HasCurrentPlayerPhase():
            current_player = world.current_player
            assert current_player, f"{self=}"
            return current_player
        elif not world.is_game_over:
            return self.GetFirstPlayer()
        else:
            return world.const_seat_order_players[0]
    def GetTurnPlayer(self) -> 'Player|None':
        from game.world.world import Phase
        world = self.GetWorld()
        if world.is_game_started and \
            world.phase.state == Phase.State.PlayerTurn:
            return world.current_player
        return None

    def GetPlayerNum(self, game_area: 'GameArea|Effect|None' = None) -> int:
        from game.operate.worlds import Worlds
        world = self.GetWorld()
        if game_area:
            return len(Worlds.GetPlayers(game_area))
        else:
            return len(world.players)

    def GetPlayerNumIcon(self) -> int:
        world = self.GetWorld()
        # return len(world.const_seat_order_players)
        if world.rule.mode_competitive:
            # L'icone « par joueur » compte les joueurs d'UNE table : les PV du
            # leader, la menace de depart d'un complot, la taille du camp. Un
            # leader affronte par un seul joueur doit avoir ses PV de base, pas
            # ceux d'une partie a deux.
            #
            # Le livret ne connait que le 1v1 et le 2v2 (mc56 p.14), et l'ecran
            # de preparation deduit les camps en coupant les sieges en deux :
            # les deux camps ont donc toujours la meme taille, et la moitie du
            # total est la taille de chacun.
            return max(1, world.started_player_num // 2)
        return world.started_player_num

    def IsThisUniqueInPlay(self, this: 'CardFace') -> bool:
        from game.operate.worlds import Worlds

        if not this.IsUnique():
            return False

        faces = Worlds.GetOnFieldCards(this.card.GetGameArea())
        for face in CardFinder(is_unique=True).Checks(faces):
            # Fix "55059"
            if face.card.state.is_defeating:
                continue
            if not this.CanCoexistWith(face):
                return True
        return False

    ################################################################################
    #
    def DiscardResourcesArea(self):
        # We need this for "23032"
        from game.effect.rule import GameRule
        from game.operate.faces import Faces
        from game.message import Message

        world = self.GetWorld()

        for player in self.const_players:
            faces = player.area_resources.GetAll(False)
            if faces:
                discarded = Faces.DiscardAll(faces, GameRule(world.GetFirstPlayer().GetIdentity()))
                # L'ordre de paiement est l'ordre des clics : la derniere carte
                # payee finit au-dessus de la defausse (Neena Thurman echange
                # avec cette carte). Le journal le dit des qu'il y a un ordre.
                if len(discarded) >= 2:
                    Message.AfterCardsPaidOrder_Text(discarded)

    def UpdatePlayersOrder(self, by_effect: 'Effect'):
        from game.message import Message
        from game.effect.rule import GameRule
        world = self.GetWorld()

        identity = self.GetFirstPlayer().GetIdentity()
        identity.SetActive(GameRule(identity))

        message = Message.AfterPlayersOrderChange(world, by_effect)
        message.Send()

    def ProcessTemporary(self, by_effect: 'Effect'):
        from game.operate.faces import Faces
        from game.operate.worlds import Worlds

        faces = Worlds.FindCardsOnField(by_effect, is_temporary=True)
        Faces.DiscardAll(faces, by_effect)

