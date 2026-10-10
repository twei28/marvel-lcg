from core import *

class VariableBool:
    def __init__(self, rules: 'WorldRule', default: bool, name: str) -> None:
        self.val = default
        self.name_true = name
        self.name_false = f"no_{name}"

        self.version = name.split('_')[0] if name.startswith(('v15', 'v16')) else None
        rules.vars_bool.append(self)

    def __bool__(self) -> bool:
        return self.val

    def Set(self, val: bool):
        self.val = val

class WorldRule:
    def __init__(self) -> None:
        self.vars_bool: List['VariableBool'] = []

        self.ex_start_hand_size     : int = 0 # scene.ex_start_hand_size, always 0
        self.disable_shuffle        : bool = False

        self.show_all_cards                 = VariableBool(self, False, "show_all_cards")
        self.disable_pay                    = VariableBool(self, False, "disable_pay")
        self.disable_limit_once             = VariableBool(self, False, "disable_limit_once")
        self.disable_game_over              = VariableBool(self, False, "disable_game_over")
        self.disable_resolve_mulligans      = VariableBool(self, False, "disable_resolve_mulligans")
        self.additional_resolve_mulligans   = VariableBool(self, False, "additional_resolve_mulligans")
        self.disable_setup_draw_cards       = VariableBool(self, False, "disable_setup_draw_cards")
        self.create_player_deck_first       = VariableBool(self, False, "create_player_deck_first")
        # Le temps d'arret sur la face A de la manigance principale (spec du
        # 15/09/2026). PAR DEFAUT A FAUX, et ce n'est pas une precaution de
        # confort : une question de plus pendant la mise en place DECALE la
        # liste des operations rejouees (engine/controller/module/replay.py,
        # controle CRC). Une sauvegarde ecrite avant ce changement ne porte pas
        # la regle, ne pose donc pas la question, et se rejoue a l'identique.
        # Seules les parties neuves lancees depuis l'ecran de preparation
        # l'allument (public/js/prepare/launcher.js, buildRules).
        self.confirm_main_scheme            = VariableBool(self, False, "confirm_main_scheme")
        # Le meme temps d'arret, pour une manigance ANNEXE que le scenario met
        # en jeu (spec du 15/09/2026, avenant). Drapeau SEPARE et non partage
        # avec la principale : une sauvegarde ecrite entre les deux ne porte que
        # le premier, et doit continuer de se rejouer sans le second.
        self.confirm_side_scheme            = VariableBool(self, False, "confirm_side_scheme")
        # L'ordre du livret pour ces temps d'arret (10/10/2026) : la face A se
        # montre des qu'elle est en jeu, avant les cartes Setup et avant ses
        # propres capacites. Drapeau SEPARE pour la meme raison que les deux
        # precedents : une sauvegarde ecrite avant pose ses questions dans
        # l'ancien ordre, et doit se rejouer dans cet ordre-la.
        self.confirm_scheme_setup_order     = VariableBool(self, False, "confirm_scheme_setup_order")

        self.v15_all                        = VariableBool(self, False, "v15_all")

        self.v16_all                        = VariableBool(self, False, "v16_all")
        self.v16_reveal                     = VariableBool(self, False, "v16_reveal")
        self.v16_teamwork                   = VariableBool(self, False, "v16_teamwork")
        self.v16_player_elimination         = VariableBool(self, False, "v16_player_elimination")
        self.v16_referential_ability        = VariableBool(self, False, "v16_referential_ability")
        self.v16_confuse_stun               = VariableBool(self, False, "v16_confuse_stun")

        self.fix_surge                      = VariableBool(self, True, "fix_surge")
        self.fix_treachery                  = VariableBool(self, True, "fix_treachery")
        self.encounter_cards_ignore_crisis  = VariableBool(self, True, "encounter_cards_ignore_crisis")
        self.crisis_of_infinite_deadpools   = VariableBool(self, True, "crisis_of_infinite_deadpools")
        self.mode_skirmish                  = VariableBool(self, False, "mode_skirmish")
        self.mode_campaign                  = VariableBool(self, False, "mode_campaign")
        # Mode competitif Civil War / Synthezoid : deux equipes de joueurs,
        # chacune avec son leader, son deck rencontre et son complot principal
        # dans sa propre zone de jeu. Pose par la liste `rules` du descripteur,
        # donc conserve dans la sauvegarde comme mode_sandbox.
        self.mode_competitive               = VariableBool(self, False, "mode_competitive")
        # Bac a sable : pose par la liste `rules` du descripteur, donc
        # conservee dans la sauvegarde — on saura toujours si une
        # victoire comptait.
        self.mode_sandbox                   = VariableBool(self, False, "mode_sandbox")
        # Mode manuel : apres la mise en place, le moteur ne conduit plus et ne
        # declenche plus rien, il tient l'etat (spec du 18/09/2026). Pose par
        # la liste `rules` du descripteur, donc conserve dans la sauvegarde :
        # on saura toujours qu'une partie n'a pas ete jouee par les regles.
        self.mode_manuel                    = VariableBool(self, False, "mode_manuel")
        self.mode_heroic                    : int = 0

    def SetRule(self, rules: List[str], is_puzzle: bool, seed: int):
        for var in self.vars_bool:
            if var.name_true in rules:
                var.Set(True)
            if var.name_false in rules:
                var.Set(False)

        self.ex_start_hand_size = 0 
        self.disable_shuffle    = seed == 0

        if is_puzzle:
            self.disable_setup_draw_cards = True
            self.disable_resolve_mulligans = True

        for rule in rules:
            if rule.startswith("mode_heroic_"):
                self.mode_heroic = int(rule.lstrip("mode_heroic_"))
                break

        if self.v16_all:
            for var in self.vars_bool:
                if var.version:
                    var.Set(var.version == "v16")

        if self.v15_all:
            for var in self.vars_bool:
                if var.version:
                    var.Set(var.version == "v15")

        # for var in self.vars_bool:
        #     if var.name_false in rules:
        #         var.Set(False)

