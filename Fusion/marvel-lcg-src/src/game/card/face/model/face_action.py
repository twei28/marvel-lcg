from core import *
from game.card.face import *
from game.ability.factory import *
from game.message import *
from game.card.face.model.base import ModelBase

class ModelAction(ModelBase):
    ################################################################################
    #
    def TreatAsIfBlank(self,
                    by_effect: 'Effect',
                    only_for_this_active_message: 'CanGainValueMessage|None'=None,
                    *,
                    until_round_end: bool=False,
                    until_phase_end: bool=False,
                    until_next_villain_phase_begin: bool=False,
                    ):
        end_event = None
        if until_round_end:
            end_event = Message.WhenRoundEnd
        if until_phase_end:
            end_event = Message.WhenPhaseEnd

        return self.TemporaryGain(
            by_effect,
            only_for_this_active_message=only_for_this_active_message,
            end_event=end_event,
            until_next_villain_phase_begin=until_next_villain_phase_begin,
            ignore_flip=True,
            treat_as_blank=True,
        )

    def TemporaryGain(self,
                    by_effect: 'Effect',
                    only_for_this_active_message: 'CanGainValueMessage|None',
                    end_event: 'Type[Message2]|None'=None,
                    # check_condition: Callable[['Effect'], bool] = lambda effect: True,
                    until_next_villain_phase_begin: bool=False,
                    *,
                    # end_at: Callable[['Effect', Callable[[], Any]], Any]|None=None,
                    # *,
                    trait: List["CardFace.TRAITS"]|"CardFace.TRAITS|None"=None,
                    #   process_fn: Callable[[int], None],
                    hand_size: int|None=None,
                    attack: int|None=None,
                    defense: int|None=None,
                    scheme: int|None=None,
                    thwart: int|None=None,
                    recover: int|None=None,
                    retaliate: int|None=None,
                    # CORRECTIF (01/09/2026, pack custom doctor_doom) :
                    # `villainous` manquait, alors que `Gain` l'accepte deja
                    # (face_gain.py:53). Meme oubli, meme correctif que
                    # `retaliate` le 4/8/2026. dd001a « Overwhelming Power »
                    # accorde villainous jusqu'a la fin du round.
                    villainous: int|None=None,
                    # CORRECTIF (02/09/2026, pack custom viv_vision) :
                    # `stalwart` manquait, alors que `Gain` l'accepte deja
                    # (face_gain.py:23). Troisieme occurrence du meme oubli,
                    # apres `retaliate` (4/8/2026) et `villainous` (1/9/2026).
                    # vv004 « Phase Up » accorde stalwart jusqu'a la fin du
                    # round : c'est le PREMIER stalwart temporaire du depot,
                    # les ~30 autres cartes qui l'accordent le font toutes par
                    # attachement permanent.
                    stalwart: int|None=None,
                    treat_as_blank: bool|None=None,
                    attack_consequential_damage: int|None=None,
                    thwart_consequential_damage: int|None=None,
                    lose_trait: "CardFace.TRAITS|None"=None,
                    ignore_flip: bool=True,
                    render_ui: bool=False,
                    # (10/10/2026, 62015 Take a Stand) : « until the end of the
                    # PLAYER phase ». Sans lui, `WhenPhaseEnd` expire au premier
                    # fin de phase venu, celle du mechant comprise.
                    end_phase: 'Literal["Player", "Villain"]|None'=None) -> None:
        from game.card.face.card_type import Ally
        from game.operate.effects import Effects
        from game.ability.condition import Condition2

        this = self.GetThis()

        # Hack for "31002a", "12033"
        if hand_size != None and this.paper.card_id in ["31002a", "31002b"]:
            faces = this.GetControlByPlayer().GetAllIdentityFace()
            for face in faces:
                if face != this:
                    face.TemporaryGain(
                        by_effect,
                        only_for_this_active_message,
                        end_event,
                        until_next_villain_phase_begin,
                        hand_size=hand_size,
                    )
                    break

        effects_temp_unit: List['Effect'] = []
        effects_temp_ally: List['Effect'] = []

        if only_for_this_active_message:
            if attack:
                # Les ICONES de boost passent par une regle (`GameRule(carte)`) et ont leur terme a part dans le calcul :
                # seuls les bonus d'EFFETS (★ d'un boost, attachement, capacite) sont nommes ici.
                from game.effect.rule import GameRule
                _source = None if isinstance(by_effect, GameRule) else getattr(by_effect, 'this', None)
                _nom = getattr(_source, 'name', None)
                _id = getattr(getattr(_source, 'card', None), 'object_id', None) or getattr(_source, 'object_id', None)
                only_for_this_active_message.AddGainedATK(attack, (_nom, _id) if _nom else None)
            if thwart:
                only_for_this_active_message.AddGainedTHW(thwart)

        if isinstance(only_for_this_active_message, Message.WhenUnitBeingAttack|Message.WhenSchemeBeingScheme):
            only_for_this_active_message = only_for_this_active_message.would_message

        # from game.card.face.attribute.can_defense import CanDefense
        # from game.card.face.attribute.can_scheme import CanScheme
        # from game.card.face.attribute.can_thwart import CanThwart
        # from game.card.face.attribute.has_hand_size import HasHandSize
        # from game.card.face.attribute.can_attack import CanAttack
        # from game.card.face.attribute.can_retaliate import CanRetaliate

        def process_fn_ally(diff: int):
            face = this.card.face
            if face.Gain(
                by_effect,
                diff,
                attack_consequential_damage=attack_consequential_damage,
                thwart_consequential_damage=thwart_consequential_damage,
            ):
                Message.AfterCardApply_Text([face], by_effect, diff)

        def process_fn(diff: int):
            face = this.card.face
            if face.Gain(
                by_effect,
                diff,
                hand_size=hand_size,
                attack=attack,
                defense=defense,
                scheme=scheme,
                thwart=thwart,
                recover=recover,
                retaliate=retaliate,
                villainous=villainous,
                stalwart=stalwart,
                treat_as_blank=treat_as_blank,
                trait=trait,
            ):
                Message.AfterCardApply_Text([face], by_effect, diff)
            if lose_trait is not None:
                face.SuppressTrait(diff, lose_trait)

            # if hand_size != None and HasHandSize.IsType(face):
            #     face.GainHandSize(hand_size * diff, by_effect)
            # if attack != None and CanAttack.IsType(face):
            #     face.GainAttack(attack * diff, by_effect, render_ui=render_ui)
            # if defense != None and CanDefense.IsType(face):
            #     face.GainDefense(defense * diff, by_effect, render_ui=render_ui)
            # if scheme != None and CanScheme.IsType(face):
            #     face.GainScheme(scheme * diff, by_effect, render_ui=render_ui)
            # if thwart != None and CanThwart.IsType(face):
            #     face.GainThwart(thwart * diff, by_effect, render_ui=render_ui)
            # if retaliate != None and CanRetaliate.IsType(face):
            #     face.GainRetaliate(retaliate * diff, by_effect)
            # if trait != None:
            #     face.GainTrait(diff, trait, by_effect)

        def unregister_effects_unit(effect: 'Effect', message: 'Message2') -> None:
            nonlocal effects_temp_unit
            Effects.UnRegister(effects_temp_unit)
            effects_temp_unit = []

        def unregister_effects_ally(effect: 'Effect', message: 'Message2') -> None:
            nonlocal effects_temp_ally
            Effects.UnRegister(effects_temp_ally)
            effects_temp_ally = []

        def unregister_effects_all(effect: 'Effect', message: 'Message2') -> None:
            unregister_effects_unit(effect, message)
            unregister_effects_ally(effect, message)

        def lost_gained_ally(effect: 'Effect', message: 'Message2') -> None:
            unregister_effects_ally(effect, message)
            if not ignore_flip:
                if this.IsInPlay():
                    process_fn_ally(-1)
            else:
                if this.card.face.IsInPlay():
                    process_fn_ally(-1)

        def lost_gained_unit(effect: 'Effect', message: 'Message2') -> None:
            unregister_effects_unit(effect, message)
            if not ignore_flip:
                if this.IsInPlay():
                    process_fn(-1)
            else:
                if this.card.face.IsInPlay():
                    process_fn(-1)

        def create_effect_interal(ability: 'Ability', *, is_ally: bool=False):
            new_effects = this.effect.Registers(
                ability
            )
            nonlocal effects_temp_unit
            nonlocal effects_temp_ally
            if is_ally:
                effects_temp_ally += new_effects
            else:
                effects_temp_unit += new_effects

        def create_effect(end_event: Type[TMP], condition: Callable[['Effect', 'TMP'], bool]):
            create_effect_interal(
                Ability(
                    AbilityType.Temp2,
                    end_event,
                    [condition],
                    lost_gained_unit
                )
            )

        def create_effect_ally(event: Type[TMP], condition: Callable[['Effect', 'TMP'], bool]):
            create_effect_interal(
                Ability(
                    AbilityType.Temp2,
                    event,
                    [condition],
                    lost_gained_ally
                ),
                is_ally=True
            )

        process_fn(+1)
        process_fn_ally(+1)

        if Ally.IsType(this):
            if isinstance(only_for_this_active_message, Message.AfterUnitAttackEnd):
                create_effect_ally(
                    Message.AfterUnitUseBasicPower,
                    lambda effect, message:
                        only_for_this_active_message == message.end_message,
                )
            if isinstance(only_for_this_active_message, Message.WhenUnitWouldAttack):
                create_effect_ally(
                    Message.AfterUnitUseBasicPower,
                    lambda effect, message:
                        isinstance(message.end_message, Message.AfterUnitAttackEnd) and \
                        only_for_this_active_message in message.end_message.would_atk_messages,
                )
            if isinstance(only_for_this_active_message, Message.WhenUnitWouldThwart):
                create_effect_ally(
                    Message.AfterUnitUseBasicPower,
                    lambda effect, message:
                        isinstance(message.end_message, Message.AfterUnitThwartEnd) and \
                        only_for_this_active_message in message.end_message.would_thw_messages,
                )
        if isinstance(only_for_this_active_message, Message.AfterUnitAttackEnd):
            create_effect(
                Message.AfterUnitAttackEnd,
                lambda effect, message:
                    only_for_this_active_message == message,
            )
        elif isinstance(only_for_this_active_message, Message.WhenUnitWouldAttack):
            create_effect(
                Message.AfterUnitAttackEnd,
                lambda effect, message:
                    only_for_this_active_message in message.would_atk_messages,
            )
        elif isinstance(only_for_this_active_message, Message.WhenUnitWouldScheme):
            create_effect(
                Message.AfterUnitSchemeEnd,
                lambda effect, message:
                    only_for_this_active_message in message.would_sch_messages,
            )
        elif isinstance(only_for_this_active_message, Message.WhenUnitWouldThwart):
            create_effect(
                Message.AfterUnitThwartEnd,
                lambda effect, message:
                    only_for_this_active_message in message.would_thw_messages,
            )
        # elif isinstance(only_for_this_active_message, Message.FakeWhenUnitWouldAttackUnit):
        #     create_effect(
        #         Message.FakeAfterUnitAttackEnd,
        #         lambda effect, message:
        #             only_for_this_active_message.would_atk_message in message.would_atk_messages,
        #     )
        elif isinstance(only_for_this_active_message, Message.WhenUnitWouldAttackUnit):
            create_effect(
                Message.AfterUnitAttackEnd,
                lambda effect, message:
                    only_for_this_active_message.would_atk_message in message.would_atk_messages,
            )
        elif isinstance(only_for_this_active_message, Message.WhenSchemeBeingThwart):
            create_effect(
                Message.AfterUnitThwartEnd,
                lambda effect, message:
                    only_for_this_active_message.would_thw_message in message.would_thw_messages,
            )
        elif isinstance(only_for_this_active_message, Message.WhenUnitUseBasicPower):
            create_effect(
                Message.AfterUnitUseBasicPower,
                lambda effect, message:
                    only_for_this_active_message == message.pre_message,
            )
        elif isinstance(only_for_this_active_message, Message.WhenUnitWouldRecovery):
            create_effect(
                Message.AfterUnitRecovery,
                lambda effect, message:
                    only_for_this_active_message == message.pre_message,
            )
        elif isinstance(only_for_this_active_message, Message.WhenPlayerPlayCard):
            create_effect(
                Message.AfterPlayerPlayedCard,
                lambda effect, message:
                    only_for_this_active_message == message.pre_message,
            )
        elif isinstance(only_for_this_active_message, Message.WhenEffectWouldResolve):
            create_effect(
                Message.AfterEffectResolved,
                lambda effect, message:
                    only_for_this_active_message == message.pre_message,
            )
        elif only_for_this_active_message == None:
            pass
        else:
            assert False, f"{only_for_this_active_message=}"

        if only_for_this_active_message:
            create_effect(
                Message.WhenMessageBeInstead,
                lambda effect, message:
                    only_for_this_active_message == message.message,
            )

        create_effect_interal(
            Ability(
                AbilityType.Temp0,
                Message.WhenUnitBeDefeated,
                [
                    Condition2.ThisIsTrigger
                ],
                unregister_effects_all
            )
        )

        if end_event == None:
            pass
        elif end_event == Message.WhenPhaseEnd:
            create_effect(
                Message.WhenPhaseEnd,
                lambda effect, message:
                    end_phase is None or message.phase_name == end_phase,
            )
        elif end_event == Message.WhenRoundEnd:
            create_effect(
                Message.WhenRoundEnd,
                lambda effect, message:
                    True,
            )
        elif end_event == Message.WhenPlayerTurnEnd:
            create_effect(
                Message.WhenPlayerTurnEnd,
                lambda effect, message:
                    True,
            )

        if until_next_villain_phase_begin == True:
            round_id = by_effect.world.round_id + 1
            create_effect_interal(
                AbilityFactory.WhenPhaseBegin(
                    AbilityType.Temp0,
                    "Villain",
                    lost_gained_unit,
                    round_id=round_id
                )
            )

        if ignore_flip:
            # create_effect_interal(
            #     AbilityFactory.AfterFlipToThisFace(
            #         AbilityType.Temp0,
            #         lambda effect, message:
            #             process_fn(+1)
            #     )
            # )
            create_effect_interal(
                Ability(
                    AbilityType.Temp0,
                    Message.AfterCardFlip,
                    [
                        lambda effect, message:
                            effect.this.card == message.trigger.card
                    ],
                    lambda effect, message:
                        process_fn(+1)
                )
            )

        create_effect_interal(
            Ability(
                AbilityType.Temp0,
                Message.WhenCardWouldFlip,
                [
                    Condition2.ThisIsTrigger
                ],
                lambda effect, message:
                    process_fn(-1)
            )
        )

        if ignore_flip:
            create_effect_interal(
                Ability(
                    AbilityType.Temp0,
                    Message.WhenCardLeavePlay,
                    [
                        Condition2.ThisIsTrigger
                    ],
                    unregister_effects_all
                )
            )
            create_effect_interal(
                Ability(
                    AbilityType.Temp0,
                    Message.AfterVillainAdvanced,
                    [
                        lambda effect, message:
                            effect.this.card == message.trigger.card
                    ],
                    lambda effect, message:
                        process_fn(+1)
                )
            )
        else:
            create_effect_interal(
                AbilityFactory.WhileThisStateUpdate(
                    AbilityType.Temp2,
                    lost_gained_unit,
                )
            )

    def GainUntilRoundEnd(self,
                          by_effect: 'Effect',
                          *,
                          trait: List["CardFace.TRAITS"]|"CardFace.TRAITS|None"=None,
                          hand_size: int|None=None,
                          attack: int|None=None,
                          defense: int|None=None,
                          scheme: int|None=None,
                          thwart: int|None=None,
                          # CORRECTIF 4/8/2026 : `retaliate` manquait alors que
                          # `TemporaryGain` l'accepte et que `GainUntilPhaseEnd`
                          # l'expose deja. Guard Protocol ab003 (pack albert)
                          # plantait sur TypeError a chaque utilisation.
                          retaliate: int|None=None,
                          # CORRECTIF (01/09/2026, pack custom doctor_doom) :
                          # `villainous` manquait ici aussi. dd001a en a besoin
                          # « until the end of the round », ce que cette
                          # methode rend exactement.
                          villainous: int|None=None,
                          # CORRECTIF (02/09/2026, pack custom viv_vision) :
                          # meme ajout que `villainous` ci-dessus, pour vv004
                          # « Phase Up » (« You gain stalwart until the end of
                          # the round »).
                          stalwart: int|None=None,
                          # CORRECTIF (02/09/2026) : `recover` manquait ICI
                          # alors que `TemporaryGain` l'accepte depuis toujours
                          # (voir sa signature juste au-dessus). Consequence :
                          # wd159 et wd160 « Web Swing! » (pack web_of_deceit)
                          # appellent `GainUntilRoundEnd(..., recover=1)`, ce
                          # qui leve un TypeError avale par le moteur. Le
                          # `Faces.ReadyAll` qui precede s'execute, donc le
                          # heros EST redresse, mais le « +1 a chaque pouvoir
                          # de base » n'arrive jamais : la carte est a moitie
                          # morte, en silence. Trouve par verifier_api_cartes.
                          recover: int|None=None,
                          # CORRECTIF (10/09/2026, pack custom iron_patriot) :
                          # meme trou que `retaliate`, `villainous`, `stalwart`
                          # et `recover` avant eux — `TemporaryGain` accepte ces
                          # deux parametres depuis toujours (voir sa signature
                          # plus haut), seul le passage manquait ici.
                          # `ip013` Call to Arms redresse des allies « and they
                          # take +1 consequential damage after they thwart or
                          # attack this round » : l'appel levait un TypeError
                          # AVALE PAR LE MOTEUR. Le `Faces.ReadyAll` qui precede
                          # passait, donc les allies etaient bien redresses et la
                          # carte avait l'air de marcher — la moitie punitive du
                          # texte, elle, n'arrivait jamais. Trouve par
                          # `tools/autoplay.py`, jamais par les cas.
                          attack_consequential_damage: int|None=None,
                          thwart_consequential_damage: int|None=None,
                          lose_trait: "CardFace.TRAITS|None"=None,
                          ignore_flip: bool=True) -> None:
        return self.TemporaryGain(
            by_effect,
            None,
            Message.WhenRoundEnd,
            trait=trait,
            hand_size=hand_size,
            attack=attack,
            defense=defense,
            scheme=scheme,
            thwart=thwart,
            retaliate=retaliate,
            villainous=villainous,
            stalwart=stalwart,
            recover=recover,
            attack_consequential_damage=attack_consequential_damage,
            thwart_consequential_damage=thwart_consequential_damage,
            lose_trait=lose_trait,
            ignore_flip=ignore_flip,
            render_ui=True
        )

    def GainUntilPhaseEnd(self,
                          by_effect: 'Effect',
                          *,
                          trait: "CardFace.TRAITS|None"=None,
                          hand_size: int|None=None,
                          attack: int|None=None,
                          defense: int|None=None,
                          scheme: int|None=None,
                          thwart: int|None=None,
                          retaliate: int|None=None,
                          ignore_flip: bool=True,
                          end_phase: 'Literal["Player", "Villain"]|None'=None) -> None:
        return self.TemporaryGain(
            by_effect,
            None,
            Message.WhenPhaseEnd,
            trait=trait,
            hand_size=hand_size,
            attack=attack,
            defense=defense,
            scheme=scheme,
            thwart=thwart,
            retaliate=retaliate,
            ignore_flip=ignore_flip,
            render_ui=True,
            end_phase=end_phase,
        )

    def GainUntilTurnEnd(self,
                          by_effect: 'Effect',
                          trait: "CardFace.TRAITS|None"=None,
                          hand_size: int|None=None,
                          attack: int|None=None,
                          defense: int|None=None,
                          scheme: int|None=None,
                          thwart: int|None=None,
                          lose_trait: "CardFace.TRAITS|None"=None,
                          ignore_flip: bool=True) -> None:
        return self.TemporaryGain(
            by_effect,
            None,
            Message.WhenPlayerTurnEnd,
            lose_trait=lose_trait,
            trait=trait,
            hand_size=hand_size,
            attack=attack,
            defense=defense,
            scheme=scheme,
            thwart=thwart,
            ignore_flip=ignore_flip,
            render_ui=True
        )

    ################################################################################
    #
    def CannotReadyDuringNextTurn(self, by_effect: 'Effect') -> None:
        from game.card.face.card_type import Identity
        from game.card.face.card_type import Ally
        assert isinstance(self, Identity|Ally)
        # TODO: Test
        self.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldReady(
                AbilityType.Temp0,
                "This",
                lambda effect, message:
                    message.SetBeInstead(by_effect)
            ),
            unregister_after_exec=False,
            until_next_turn_end=True
        )

