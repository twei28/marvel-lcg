from core import *
from game.card.face.base import *
from game.card.face import *
from game.ability import *
from game.ability.factory import *
from game.message import *
from game.player import *
from cards.paper import Paper

class Enemy(HasScheme, CanScheme, HasAttack, CanAttack, CanHinder, HasThreatLevel, Unit2, CanBoost, CanPlaceCounter):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    ################################################################################
    # Un heros peut etre ACCROCHE a cet ennemi (Alligator Loki, voir
    # `Hero.attached_enemy` dans card_type/identity.py). Rend le numero
    # d'affichage du joueur (player_id + 1) dont le heros tient cet ennemi,
    # 0 sinon : c'est le marqueur que l'interface pose sur la carte ennemie.
    def GetHoldingHeroPlayerNumber(self) -> int:
        from game.card.face.card_type.identity import Hero, Identity
        for player in self.card.world.const_players:
            if player.area_hero.GetSize() == 0:
                continue
            identity = player.area_hero.Get()[0]
            if not Identity.IsType(identity):
                continue
            # ⚠ `FindHeroFace`, pas `GetHeroFace` : Peni Parker (SP//dr) n'a pas
            # de face heros sur sa carte, et ce rendu tourne pour CHAQUE ennemi
            # de CHAQUE partie. L'assert de `GetHeroFace` a tue toutes les
            # parties de SP//dr du 01/09 au 11/09/2026. Sans face heros, ce
            # joueur ne tient rien.
            hero = identity.CastTo(Identity).FindHeroFace()
            if hero is not None and hero.GetHeldEnemy() is self:
                return player.player_id + 1
        return 0

    @override
    def GetInfoDict(self) -> Dict[str, int]:
        return super().GetInfoDict() | {
            'held_by_hero': self.GetHoldingHeroPlayerNumber(),
        }

    ################################################################################
    #
    def DoSchemes(self, against_player: 'Player', by_effect: 'Effect', *,
                    property: 'SchemeProperty|None'=None,
                    operation: Callable[['Message.WhenUnitWouldScheme'], Any]|None=None,
                    for_each_threat_placed: Callable[[int], None|Any]|None=None,
                    ) -> 'Message.AfterUnitSchemeEnd|None':
        from game.operate.worlds import Worlds
        from game.operate.effects import Effects
        from game.operate.run_at import RunAt
        from game.effect.rule import GameRule
        from game.message.message_type import InActivationMessage
        scheme = Worlds.FindMainScheme(self)
        if not scheme:
            return None

        bind_message = by_effect.bind_message 
        if isinstance(bind_message, InActivationMessage) and \
            bind_message.activate_message and \
            not bind_message.activate_message.is_be_instead:
            RunAt.AfterEnemyActivationEnd(
                by_effect,
                bind_message.activate_message,
                lambda:
                    self.DoSchemes(
                        against_player,
                        GameRule(by_effect.this),
                        property=property,
                        operation=operation,
                    )
            )
            return

        action_effects: List['Effect'] = []
        if operation:
            action_effects += by_effect.this.effect.RegisterTemp(
                AbilityFactory.WhenUnitWouldScheme(
                    AbilityType.Temp0,
                    None,
                    lambda effect, message:
                        operation(message),
                    by_effect=by_effect,
                ),
                unregister_after_exec=False
            )

        if property == None:
            property = SchemeProperty(is_basic_power=True, against_player=against_player)
        else:
            property.against_player = against_player

        return_value = self.BasicSchemes(by_effect, property=property)
        Effects.UnRegister(action_effects)

        if for_each_threat_placed and return_value and return_value.placed_threat > 0:
            for_each_threat_placed(return_value.placed_threat)

        return return_value

    def DoAttackYou(self, against_player: 'Player|Literal["YourLeader"]', by_effect: 'Effect', *,
                    property: 'AttackProperty|None'=None,
                    operation: Callable[['Message.WhenUnitWouldAttack'], Any]|None=None,
                    operation_end: Callable[['Message.AfterUnitAttackEnd'], Any]|None=None,
                    if_no_character_takes_damage: Callable[[], None]|None=None,
                    if_characters_damaged_by_this: Callable[[List['Unit2']], None|int]|None=None,
                    if_this_attack_deals_damage: Callable[[int], None|Any]|None=None,
                    if_no_attack_was_made: Callable[[], None]|None=None,
                    if_unit_defends_against: Callable[['Unit2', int], None]|None=None,
                    if_undefended: Callable[[], None]|None=None,
                    you_cannot_play_event: bool=False,
                    other_characters_cannot_defend: bool=False,
                    ) -> 'Message.AfterUnitAttackEnd|None':
        from game.card.face.card_type import Event
        from game.operate.effects import Effects
        from game.operate.run_at import RunAt
        from game.effect.rule import GameRule
        from game.message.message_type import InActivationMessage

        if against_player == "YourLeader":
            if if_no_character_takes_damage:
                if_no_character_takes_damage()
            if if_no_attack_was_made:
                if_no_attack_was_made()
            return None

        bind_message = by_effect.bind_message 
        if isinstance(bind_message, InActivationMessage) and \
            bind_message.activate_message and \
            not bind_message.activate_message.is_be_instead:
            RunAt.AfterEnemyActivationEnd(
                by_effect,
                bind_message.activate_message,
                lambda:
                    self.DoAttackYou(
                        against_player,
                        GameRule(by_effect.this),
                        property=property,
                        operation=operation,
                        operation_end=operation_end,
                        if_no_character_takes_damage=if_no_character_takes_damage,
                        if_characters_damaged_by_this=if_characters_damaged_by_this,
                        if_this_attack_deals_damage=if_this_attack_deals_damage,
                        if_no_attack_was_made=if_no_attack_was_made,
                        if_unit_defends_against=if_unit_defends_against,
                        if_undefended=if_undefended,
                        you_cannot_play_event=you_cannot_play_event,
                        other_characters_cannot_defend=other_characters_cannot_defend,
                    )
            )
            return

        action_effects: List['Effect'] = []
        if operation:
            action_effects += by_effect.this.effect.RegisterTemp(
                AbilityFactory.WhenUnitWouldAttack(
                    AbilityType.Temp0,
                    self,
                    lambda effect, activate_message:
                        operation(activate_message),
                    by_effect=by_effect,
                ),
                unregister_after_exec=False
            )
        if you_cannot_play_event:
            action_effects += by_effect.this.effect.RegisterTemp(
                AbilityFactory.PlayersCannotPlayCardWhile(
                    against_player,
                    Event,
                ).NoOutOfPlayLimit(),
                unregister_after_exec=False
            )

        identity = against_player.GetIdentity()
        if other_characters_cannot_defend:
            action_effects += by_effect.this.effect.RegisterTemp(
                *AbilityFactory.UnitCannotDefend(
                    CardFinder(non_face=identity),
                    self,
                    cannot_trigger_defense_ability=True,
                ),
                unregister_after_exec=False
            )

        if property == None:
            property = AttackProperty(is_basic_power=True, against_player=against_player)
        else:
            property.against_player = against_player

        return_val = self.BasicAttack([identity], by_effect,
                                        property=property,
                                        if_no_character_takes_damage=if_no_character_takes_damage,
                                        if_characters_damaged_by_this=if_characters_damaged_by_this,
                                        for_each_damage_dealt_by_this=if_this_attack_deals_damage,
                                        if_no_attack_was_made=if_no_attack_was_made,
                                        if_unit_defends_against=if_unit_defends_against,
                                        if_undefended=if_undefended,
                                        )

        if operation_end and return_val:
            operation_end(return_val)

        Effects.UnRegister(action_effects)
        return return_val

    ################################################################################
    # BRIQUE COMMUNE (20/10/2026) : « un ennemi attaque un autre ennemi ou un
    # allie » (campagnes Punisher MC×DC et Galactic Storm). Recette :
    # docs/reference/RECETTES-MOTEUR.md §15.1.
    #
    # Une ATTAQUE DE BASE de cet ennemi contre `target`, qui peut etre un allie,
    # un sbire, le mechant ou un autre mechant, une identite. Les degats et
    # l'exces (overkill) tombent sur la cible. Ce qui distingue cette entree de
    # `BasicAttack([cible])`, dont elle se sert :
    #
    # - cible ENNEMIE : aucun joueur n'est attaque (`against_player` None, les
    #   capacites « attacks you » ne partent pas), et `for_player` est le
    #   « vous » des Boost (Galactic Storm p.9 : le joueur qui a revele la carte
    #   qui provoque l'attaque ; par defaut, le joueur de l'effet ou le premier
    #   joueur). Personne ne defend, sauf `players_may_defend=True` (Punisher
    #   p180) ; le defenseur devient alors la cible.
    # - cible ALLIEE : le controleur est le joueur attaque et peut defendre
    #   (Rules Reference 1.8 p.10, « Attacks Against Allies »).
    #   `ally_attack_is_against_player=False` applique la variante de Galactic
    #   Storm p.4 (« attacks you » ne part pas) : question ouverte, voir
    #   `.planning/todos/2026-10-20-briques-communes-questions.md`.
    # - `overkill` : True/False force le mot-cle pour CETTE attaque (None :
    #   celui que l'attaque a deja). `overkill_to` : la cible de l'exces quand
    #   le coup abat un SBIRE (face, ou fonction `(sbire) -> face`) ; None =
    #   « le mechant » (RR 1.8 p.31).
    # - `additional_attack` : « attacks ... with +2 ATK » (Punishment p213).
    # - `give_boost=False` : « do not give him a boost card ».
    #
    # PAS de report apres l'activation en cours (contrairement a
    # `DoAttackYou`) : l'appelant qui remplace une activation (« attacks X
    # instead ») l'appelle depuis son interruption, apres `SetBeInstead`.
    def AttackCharacter(self, target: 'CardFace', by_effect: 'Effect', *,
                        for_player: 'Player|None'=None,
                        players_may_defend: bool=False,
                        ally_attack_is_against_player: bool=True,
                        overkill: bool|None=None,
                        overkill_to: 'CardFace|Callable[[CardFace], CardFace|None]|None'=None,
                        additional_attack: int=0,
                        give_boost: bool=True,
                        ignore_boost_abilities: bool=False,
                        property: 'AttackProperty|None'=None,
                        if_this_defeat_unit: Callable[['CardFace'], None]|None=None,
                        if_no_attack_was_made: Callable[[], None]|None=None,
                        if_characters_damaged_by_this: Callable[[List['Unit2']], None|int]|None=None,
                        ) -> 'Message.AfterUnitAttackEnd|None':
        from game.card.face.base import Friend
        from game.card.face.card_type import Minion
        from game.operate.worlds import Worlds

        if target is None:
            if if_no_attack_was_made:
                if_no_attack_was_made()
            return None
        target = target.card.face

        if property is None:
            property = AttackProperty(is_basic_power=True)
        property.additional_value += additional_attack
        if not give_boost:
            property.do_not_give_boost = True
        if ignore_boost_abilities:
            property.ignore_boost_abilities = True
        if overkill is not None:
            property.overkill = overkill

        controleur = target.GetControlBy()
        if Friend.IsType(target) and Player.IsType(controleur):
            property.boost_player = controleur
            if not ally_attack_is_against_player:
                property.not_against_player = True
        else:
            # Cible ennemie : aucun joueur attaque.
            property.not_against_player = True
            property.against_player = None
            if for_player is None:
                # `initiator` brut : `GetInitiator()` exige un joueur (assert).
                initiateur = getattr(by_effect, 'initiator', None)
                for_player = initiateur if Player.IsType(initiateur) else Worlds.GetFirstPlayer(by_effect)
            property.boost_player = for_player
            property.players_may_defend = players_may_defend

        if overkill_to is not None:
            def cible_de_l_exces(abattu: 'Unit2') -> 'Unit2|None':
                if Minion.IsType(abattu):
                    face = overkill_to(abattu) if callable(overkill_to) else overkill_to
                    return face.card.face if face is not None else None
                return CanAttack.DefaultOverkillTarget(abattu, by_effect)
            property.overkill_target_fn = cible_de_l_exces

        return self.BasicAttack([target], by_effect,
                                property=property,
                                if_this_defeat_unit=if_this_defeat_unit,
                                if_no_attack_was_made=if_no_attack_was_made,
                                if_characters_damaged_by_this=if_characters_damaged_by_this)

    def DoActivate(self, against_player: 'Player', by_effect: 'Effect', operation: Callable[['Message.WhenEnemyActivateAgainstYou'], Any]|None=None, do_not_give_boost: bool=False, if_no_activate: Callable[[], Any]|None=None) -> 'Message.AfterUnitAttackEnd|Message.AfterUnitSchemeEnd|None':
        from game.operate.effects import Effects

        if operation:
            action_effects = by_effect.this.effect.Registers(
                AbilityFactory.WhenEnemyActivateAgainstYou(
                    AbilityType.Temp0,
                    None,
                    lambda activate_effect, message:
                        operation(message),
                    conditions=[
                        lambda activate_effect, activate_message:
                            self == activate_message.trigger and \
                            by_effect == activate_message.by_effect
                    ],
                )
            )
        else:
            action_effects = None

        would_act_message = Message.WhenEnemyWouldActivate(self, against_player)
        would_act_message.Send()
        if would_act_message.is_be_instead:
            from game.card.face.attribute.can_attack import CanAttack
            CanAttack.JournaliserActivationEmpechee(self, against_player, would_act_message)
            return None

        if against_player.IsAlterEgo():
            message = self.DoSchemes(against_player, by_effect, property=SchemeProperty(against_player=against_player, do_not_give_boost=do_not_give_boost, would_act_message=would_act_message))
        else:
            message = self.DoAttackYou(against_player, by_effect, property=AttackProperty(against_player=against_player, do_not_give_boost=do_not_give_boost, would_act_message=would_act_message))

        Effects.UnRegister(action_effects)

        if not message:
            if if_no_activate:
                if_no_activate()

        return message
