from core import *
from game.ability import *
from game.card.face import *
from game.player import *
from game.world import *

class PlayerSideSchemeLimit:

    def __init__(self, world: 'World') -> None:
        self.world = world

    def CheckLimit(self, chooser: 'Player|None' = None) -> bool:
        from game.operate.faces import Faces
        from game.effect.rule import GameRule
        from game.card.card_finder import CardFinder
        from game.card.face.card_type import PlayerSideScheme
        from game.ability.factory import AbilityFactory

        world = self.world

        limit_num = (world.started_player_num+1) // 2

        max_repeat_times = 10
        while True:
            assert max_repeat_times > 0
            max_repeat_times -= 1

            if world.is_game_over:
                return False

            # RR 1.8 p.33 : c'est le joueur qui met en jeu la manigance au-dela de la
            # limite qui choisit celle a defausser (avant : toujours le premier joueur).
            player = chooser if chooser is not None and world.rule.v18_side_scheme_limit and not chooser.is_eliminated \
                else world.GetFirstPlayer()
            # CORRECTIF (ajout volontaire) : les player side schemes marqués
            # not_count_player_side_scheme_limit (schemes campagne NeXt Evolution,
            # « does not count against the player side scheme limit ») sont exclus.
            faces = [x for x in world.area_schemes_side.Get(True) if PlayerSideScheme.IsType(x) and not getattr(x, 'not_count_player_side_scheme_limit', False)]
            exceed_num = len(faces) - limit_num

            rule = GameRule(player.GetIdentity())

            def action(targets: Sequence['CardFace']):
                Faces.DiscardAll(targets, rule)

            if exceed_num > 0:
                player.ChooseAbilities(
                    rule,
                    AbilityFactory.ForChoiceAbility(
                        "Player Side Scheme Limit",
                        action,
                    ).SetTarget(faces, finder=CardFinder(canbe_discard=True))
                )
            else:
                break
        return True

