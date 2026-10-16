from typing import TypeAlias
from core import *
from game.card.face import *
from game.effect import *
from game.selector import *
from game.player import *
from game.message import *
from game.element.resources import Resources
from game.element.cost import Cost
# from game.ability.condition import Condition
from game.card.card_finder import CardFinder

TARGET_TYPE: TypeAlias = 'SELECT.HELPER_TYPE|Selector|CardFinder'

def TakeDamageOnCall(targets: Sequence['CardFace'], damage: int, effect: 'Effect') -> bool:
    from game.card.face.base import Unit2
    # If taking damage is a cost, that cost is not considered
    # paid unless all of that damage was taken. (If any of
    # the damage is prevented, then the cost has not been
    # paid.)
    this = effect.this
    for target in targets:
        unit = target.CastTo(Unit2)
        message = unit.TakeDamage(this, damage, effect)
        if message == None:
            return False
        if message.took_damage != damage:
            return False
        # ⚠ ON NE REFUSE PLUS LE COUT QUAND LE PAYEUR EN MEURT (correctif du
        # 10/09/2026, pack spider_woman_kajislav).
        #
        # Il y avait ici `if unit.IsDefeated(): return False`, sans un mot pour
        # l'expliquer, alors que le commentaire ci-dessus ne couvre QUE les
        # degats EMPECHES — la citation de la regle officielle porte sur eux et
        # sur rien d'autre. La ligne allait plus loin qu'elle : un cout paye
        # jusqu'au bout etait declare impaye au seul motif que le personnage
        # tombait.
        #
        # CE QUE CELA RENDAIT IMPOSSIBLE : `sw013` Shroud, allie a 2 PV dont le
        # cout imprime est « inclinez Shroud et infligez-lui 2 degats ». Le
        # cout le tue A TOUS LES COUPS, par construction : la carte etait donc
        # INERTE, elle payait son prix et ne faisait jamais rien. Aucune trace,
        # aucune exception. C'est un consommable, pas un accident de reglage.
        #
        # Les autres appelants visent l'identite (`45043`, `45050`, `01027`,
        # `bl009`) : une identite qui tombe fait perdre la partie, la question
        # de savoir si la capacite resout est alors sans objet. Le garde-fou
        # propre a l'identite existe d'ailleurs a part, dans
        # `TakeIndirectDamage` (`return not identity.IsDefeated()`), et il n'est
        # pas touche.
    return True

class CostFunc:

    class Base:
        def __init__(self, selector: 'Selector', call_fn: Callable[[Sequence['CardFace'], 'Effect', 'Player|None'], bool]|None, check_fn: Callable[['Effect'], None|Literal[True]]|None=None) -> None:
            self.selector = selector
            self.call_fn = call_fn
            self.check_fn = check_fn
            if self.selector:
                self.selector.selector_end.not_move = True
            self.cost_legal_targets: Sequence[CardFace] = []
            pass

        def OnEffectEnd(self, targets: Sequence['CardFace'], effect: 'Effect'):
            pass

        @final
        def HasTargets(self, effect: 'Effect') -> bool:
            if self.check_fn and self.check_fn(effect):
                return True
            if self.selector:
                return self.selector.HasLegalTargets(effect)
            else:
                return True

        @final
        def PayCost(self, effect: 'Effect', player: 'User') -> bool:
            from game.player import Player

            # ⚠ A CHAQUE APPEL, MEME CELUI QUI VA ECHOUER (20/09/2026). L'objet
            # CostFunc appartient a l'ABILITY, que `CardsDB.FindAbilities` sert
            # TELLE QUELLE a toutes les copies d'un meme `card_id` et a tous les
            # joueurs. Ce qu'il retient d'un paiement survivrait donc au suivant,
            # et `SpendResource` rendrait un cout que ce paiement-ci n'a jamais
            # paye. On repart de zero avant de rien engager.
            self.ResetCostSnapshot()

            can_be_zero = False
            num_range = None
            if effect.ability.flags.is_check_pay:
                targets = self.selector.GetAllLegalTargets(effect, just_check=True)
            else:
                targets = self.selector.GetAllLegalTargets(effect, just_check=True)
                num_range = self.selector.GetTargetRange(effect, targets)
                if num_range:
                    if num_range[0] == 0:
                        can_be_zero = True
                    if len(targets) < num_range[0]:
                        targets = []
                    elif len(targets) == num_range[0] and targets and targets[0].IsInDeck():
                        targets = targets[:num_range[0]]
                    elif len(targets) == num_range[0] and targets:
                        # ⚠⚠ RACCOURCI GENERALISE (25/09/2026, demande de
                        # l'utilisateur : « trop cliquer » sur She-Devil de
                        # Red Sonja -- rs001a/rs002 -- et ~18 autres cartes au
                        # meme motif). Le cas juste au-dessus (`IsInDeck()`)
                        # sautait deja la demande au joueur quand il n'y a pas
                        # de vrai choix pour une carte DU DECK ; le meme
                        # raisonnement vaut pour n'importe quelle carte : des
                        # que le nombre de cibles LEGALES egale le nombre
                        # EXIGE, prendre les unes ou les autres n'est pas un
                        # choix, c'est une formalite. La demander quand meme
                        # coute un aller-retour reseau et un clic pour rien.
                        # Meme convention que `ChooseOrder()`
                        # (player_ask.py), qui a ce raccourci depuis
                        # longtemps pour un besoin voisin
                        # (`if len(faces) == 1: return list(faces)`).
                        #
                        # ⚠ ON NE TOUCHE PAS a la branche `IsInDeck()`
                        # ci-dessus : elle existe depuis le moteur d'origine,
                        # sans commentaire pour en expliquer la portee
                        # exacte -- ce nouveau cas s'ajoute a cote plutot que
                        # de la generaliser sur place, pour ne rien changer
                        # a son comportement deja verifie.
                        targets = targets[:num_range[0]]
                    else:
                        if self.selector.selector_rule.random:
                            targets = self.selector.GetRandomTarget(targets, effect)
                            targets = targets[:num_range[0]]
                        elif isinstance(player, Player):
                            targets = player.AskChooseFaces(targets, num_range, effect, prompt=f"Pay cost {self}")
                else:
                    targets = []

            self.cost_legal_targets = targets[:]

            if targets == [] and self.selector and not can_be_zero:
                return False

            if num_range and not self.selector.AfterSelectTargets(effect, targets, num_range):
                return False

            # We don't process the cost when checking pay
            # we will handle the cost in `DoGenerateResources`
            if self.call_fn and not effect.ability.flags.is_check_pay:
                return self.call_fn(targets, effect, player if isinstance(player, Player) else None)
            return True

        def ResetCostSnapshot(self) -> None:
            """Oublie le paiement precedent. Voir `PayCost`, qui l'appelle."""
            pass

        def SnapshotCost(self, effect: 'Effect') -> Any:
            """CE QUE CE PAIEMENT-CI VIENT D'ENGAGER, releve tout de suite.

            `SpendResource` appelle ce releve juste apres chaque payeur, et le
            rend tel quel a `RollbackCost` si le paiement est abandonne. On ne
            relit JAMAIS l'etat de l'objet CostFunc au moment du rendu : il est
            partage entre toutes les copies de la carte, et deux copies qui
            paient le meme cout se l'ecrasent l'une l'autre -- la premiere
            resterait inclinee pour toujours, en silence.
            """
            return None

        def RollbackCost(self, effect: 'Effect', releve: Any) -> bool:
            """REND ce que `PayCost` a engage, quand le paiement est ABANDONNE.

            Appelee par `Player.SpendResource` (player_action.py) et par elle
            seule : un paiement qui ne couvre pas le cout ne doit rien couter
            au joueur. Rend True quand il n'y a plus rien a rendre, False
            quand ce cout-la ne sait pas se defaire -- l'appelant le journalise
            alors, il ne l'ignore pas en silence.

            Le cas par defaut : un cout SANS `call_fn` n'a fait que CHOISIR des
            cibles, il n'a rien preleve, il n'y a donc rien a rendre.
            """
            return self.call_fn == None

        @final
        def AfterCheck(self, effect: 'Effect'):
            self.OnEffectEnd(self.cost_legal_targets, effect)

        @final
        def __repr__(self) -> str:
            return self.__class__.__name__

    # class Either(Base):
    #     def __init__(self, call_fn: Callable[['Effect'], bool]) -> None:
    #         self.return_value: Any = None
    #         def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None'):
    #             return call_fn(effect)
    #         super().__init__(Select("This"), on_call)
    #         pass

    # class DoNothing(Base):
    #     def __init__(self) -> None:
    #         selector = Select.From("This")
    #         self.return_value: Any = None
    #         super().__init__(selector, None)

    # class Or(Base):
    #     def __init__(self, *abilities: 'Ability') -> None:
    #         self.return_value: Any = None
    #         def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None'):
    #             initiator = effect.GetInitiator()
    #             select_effect = initiator.ChooseAbilities(
    #                 effect,
    #                 *abilities
    #             )
    #             return select_effect != None
    #         selector = Select.From("This")
    #         super().__init__(selector, on_call)

    class Custom(Base):
        def __init__(self, selector: 'Selector|CardFinder|None', call_fn: Callable[[Sequence['CardFace'], 'Effect'], bool]) -> None:
            self.return_value: Any = None
            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None'):
                return call_fn(targets, effect)
            if selector == None:
                selector = Select.From("This")
            elif isinstance(selector, CardFinder):
                selector = Select.From(selector)
            super().__init__(selector, on_call)

    class LookAtDeck(Base):
        def __init__(self, deck_name: Literal["YourPlayerDeck", "EncounterDeck"], size: int, *, discard:int=0) -> None:
            from game.operate.worlds import Worlds
            from game.card.card_finder import CardFinder

            self.return_look_at_cards: List['CardFace'] = []
            self.return_discard_cards: List['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                if deck_name == "YourPlayerDeck":
                    deck = player.player_deck
                elif deck_name == "EncounterDeck":
                    deck = Worlds.GetEncounterDeck(effect)

                faces = player.LookAtDeck(deck, size, effect)
                self.return_look_at_cards = list(faces)

                if discard:
                    self.return_discard_cards = player.AskDiscardFaces(faces, (discard, discard), effect, not_shuffle=True)
                return True

            # This condition doesn't use `face`, should we still put it here?
            def has_enought_size(effect: 'Effect', face: 'CardFace') -> bool:
                initiator = effect.GetInitiator()
                if deck_name == "YourPlayerDeck":
                    deck = initiator.player_deck
                elif deck_name == "EncounterDeck":
                    deck = Worlds.GetEncounterDeck(effect)
                return deck.GetSize() >= size

            selector = Select.From("This", finder=CardFinder(check_effect_fn=has_enought_size))
            super().__init__(selector, on_call)

    class Exhaust(Base):
        def __init__(self,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,
                    has_confuse_status: bool|None=None,
                    share_trait_with_your_hero: bool=False,
                    share_trait_with_your_identity: bool=False,
                    from_where: List['SELECT.WHERE']=["Default"],
                    range: 'SELECT.RANGE_TYPE'=(1, 1),
                    ) -> None:
            from game.operate.faces import Faces
            from game.card.card_finder import CardFinder
            self.return_exhausted_cards: List['CardFace'] = []
            self.not_need_to_exhaust: List['CardFace'] = []
            # ⚠ RETENU POUR LA GATE, pas pour le jeu : incliner « This » suppose
            # que la carte est DEJA EN JEU. Une capacite de mise en jeu
            # (`SetPlay`) qui reclamerait ce cout serait injouable pour
            # toujours. `Ability.SetPlay` / `SetCostFunc` le refusent en lisant
            # ce drapeau. Voir game/ability/ability.py.
            self.exige_cette_carte_en_jeu = (target == "This")

            def on_check(effect: 'Effect'):
                if self.not_need_to_exhaust:
                    return True

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if self.not_need_to_exhaust:
                    return True
                if Faces.ExhaustAll(targets, effect) == targets:
                    self.return_exhausted_cards = list(targets)
                    return True
                else:
                    return False

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                        has_confuse_status=has_confuse_status,
                    ),
                    share_trait_with_your_hero=share_trait_with_your_hero,
                    share_trait_with_your_identity=share_trait_with_your_identity,
                    range=range,
                    from_where=from_where
                )
            # CORRECTIF (16/10/2026, aspect TMNT Protection, up041 Usagi Yojimbo) : un cout d'inclinaison
            # rendu inutile (`not_need_to_exhaust`, « does not exhaust to defend » : 53011 Draw Their Fire,
            # up041) doit rester payable par une carte DEJA inclinee. Rules Reference v1.8, « Defending » :
            # « A card ability that allows an ally to be declared as a defender without exhausting can be
            # used on an exhausted ally. » `on_check` le disait deja ; le filtre `canbe_exhaust=True` du
            # selecteur, lui, retirait la carte inclinee des cibles et `PayCost` echouait. Liste vide (tous
            # les autres couts) : filtre identique a l'ancien.
            selector.selector_filter.AddParameter(
                check_effect_fn=lambda effect, face: face.CanExhaust() or bool(self.not_need_to_exhaust))
            super().__init__(selector, on_call, on_check)

        def ResetCostSnapshot(self) -> None:
            self.return_exhausted_cards = []

        def SnapshotCost(self, effect: 'Effect') -> Any:
            # Une COPIE : la liste de l'objet CostFunc sera reecrite par le
            # prochain payeur, y compris une autre copie de la meme carte dans
            # ce meme paiement.
            return list(self.return_exhausted_cards)

        def RollbackCost(self, effect: 'Effect', releve: Any) -> bool:
            """REDRESSE les cartes que ce paiement-ci vient d'incliner.

            Le seul rendu EXACT possible : le releve est la liste precise des
            cartes inclinees par ce payeur, et une carte inclinee pour payer se
            rend en la redressant.
            """
            from game.operate.faces import Faces
            if releve:
                Faces.ReadyAll(releve, effect)
            return True

    # class Choose2(Base):
    #     def __init__(self, traits: List["CardFace.TRAITS"],
    #                 *,
    #                 do_exhaust: bool=False,
    #                 do_return_to_owner_hand: bool=False) -> None:
    #         from game.card.face.faces import Faces
    #         from game.card.card_finder import CardFinder
    #         self.return_exhausted_cards: List['CardFace'] = []

    #         def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
    #             if do_exhaust:
    #                 if Faces.ExhaustAll(targets, effect) == targets:
    #                     self.return_exhausted_cards = list(targets)
    #                     return True
    #             if do_return_to_owner_hand:
    #                 if Faces.ReturnToHand(targets, "Owner", effect) == targets:
    #                     self.return_exhausted_cards = list(targets)
    #                     return True
    #             return False

    #         selector = Select(None,
    #             CardFinder(traits=traits),
    #             range=(2, 2),
    #             select_rule="MustIncludeTraits"
    #         )

    #         if do_exhaust:
    #             for finder in selector.finders:
    #                 finder.canbe_exhaust = True
    #         super().__init__(selector, on_call)

    class ResolveAbility(Base):
        def __init__(self, 
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None
                    ) -> None:
            from game.card.card_finder import CardFinder
            self.return_exhausted_cards: List['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                resolved = False
                for target in targets:
                    resolved |= target.ResolveSpecialAbility(player, effect)
                return resolved

            selector = Select.From(
                CardFinder(
                    name=name,
                    trait=trait,
                    card_type=card_type,
                ),
            )
            super().__init__(selector, on_call)

    # class ExhaustThis(Base):
    #     def __init__(self) -> None:
    #         self = CostFunc.Exhaust("This")

    class AttackYou(Base):
        def __init__(self,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,) -> None:
            from game.card.face.attribute.can_attack import CanAttack
            from game.card.face.base import Enemy
            from game.card.card_finder import CardFinder

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                do_attack = False
                for target in targets:
                    if Enemy.IsType(target):
                        if target.DoAttackYou(player, effect) != None:
                            do_attack = True
                    elif CanAttack.IsType(target):
                        if target.BasicAttack([player.GetIdentity()], effect) != None:
                            do_attack = True

                return do_attack

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                    ),
                )
            selector.selector_filter.AddParameter(canbe_exhaust=True)
            super().__init__(selector, on_call)

    class Ready(Base):
        def __init__(self,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    ) -> None:
            from game.operate.faces import Faces
            from game.card.card_finder import CardFinder
            self.return_readied_cards: List['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if Faces.ReadyAll(targets, effect) == targets:
                    self.return_readied_cards = list(targets)
                    return True
                else:
                    return False

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                    ),
                )
            selector.selector_filter.AddParameter(canbe_ready=True)
            super().__init__(selector, on_call)

    class DealDamage(Base):
        def __init__(self, value: int,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,
                    another: bool|None=None, # Not `effect.this`
                    # selector: 'Selector|None'=None,
                    ) -> None:
            from game.card.face.base import Unit2
            from game.card.card_finder import CardFinder
            self.return_damaged_units: List['Unit2'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                self.return_damaged_units = []
                # If dealing damage is a cost, that cost is considered
                # paid even if some or all of that damage is prevented.
                if effect.this.DealDamage(targets, value, effect) != None:
                    for target in targets:
                        if Unit2.IsType(target):
                            self.return_damaged_units.append(target)
                    return True
                else:
                    return False
                # return not this.IsDefeated()

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                    ),
                    another=another,
                )
            selector.selector_filter.AddParameter(has_non_health=False)
            super().__init__(selector, on_call)

            # def unit_can_take_damage(effect: 'Effect', message: 'Message2') -> bool:
            #     targets = self.GetTargets(effect, self.who)
            #     if targets == []:
            #         return False
            #     for target in targets:
            #         if not Unit2.IsType(target):
            #             return False
            #     return True
            # return unit_can_take_damage

    class TakeDamage(Base):
        def __init__(self, value: int|Callable[['Effect'], int],
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,) -> None:
            from game.card.card_finder import CardFinder

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not isinstance(value, int):
                    damage = value(effect)
                else:
                    damage = value

                return TakeDamageOnCall(targets, damage, effect)

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                    ),
                )
            selector.selector_filter.AddParameter(has_non_health=False)
            super().__init__(selector, on_call)

    class TakeIndirectDamage(Base):
        def __init__(self, value: int|Callable[['Effect'], int]) -> None:

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                nonlocal value

                if not player:
                    return False
                this = effect.this
                if not isinstance(value, int):
                    damage = value(effect)
                else:
                    damage = value
                identity = player.GetIdentity()
                identity.TakeIndirectDamage(this, damage, effect)
                return not identity.IsDefeated()

            selector = Select.From("This")
            super().__init__(selector, on_call)

    # @staticmethod
    # # param int
    # def TakeDamageUpTo(effect: 'Effect') -> bool:
    #     def deal_damage_to_this(effect: 'Effect') -> bool:
    #         unit = get_unit(effect)
    #         player = unit.GetControlByPlayer()
    #         damage = player.NameNumber(1, param)
    #         unit.TakeDamage(unit, damage, effect)
    #         return not unit.IsDefeated()
    #     self.cost_funcs.append(deal_damage_to_this)

    class TakeDamageUpToHealth(Base):
        def __init__(self, target: 'TARGET_TYPE|None'=None) -> None:
            self.return_damage: int = 0

            def has_enough_health(effect: 'Effect', face: 'CardFace') -> bool:
                # if Unit2.IsType(face):
                #     return face.health > 1
                # return False
                return True

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                damage = player.DeclareNumber(1, player.GetIdentity().health)

                if TakeDamageOnCall(targets, damage, effect):
                    # For "44004"
                    self.return_damage = damage
                    return True
                else:
                    return False

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(target)
            selector.selector_filter.AddParameter(has_non_health=False, check_effect_fn=has_enough_health)
            super().__init__(selector, on_call)

    # Heal
    class Heal(Base):
        def __init__(self, damage: int,
                    target: 'TARGET_TYPE|None'=None,
                    ) -> None:
            self.return_targets: Sequence['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                self.return_targets = targets
                return effect.this.HealthUnits(targets, damage, effect) >= damage

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(target)
            selector.selector_filter.AddParameter(canbe_heal=damage)
            super().__init__(selector, on_call)

    # DealPlayerFacedownEncounterCard
    class DealPlayerEncounterCard(Base):
        def __init__(self, value: int,
                    target: Literal["Initiator", "FirstPlayer", "AnyPlayer"],
                    ) -> None:
            from game.player import Player
            self.return_players: List[Player] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                self.return_players = []

                for target in targets:
                    self.return_players.append(target.GetControlByPlayer())
                for player in self.return_players:
                    player.DealEncounterCards(value, effect)
                return True

            if target == "AnyPlayer":
                select_target = "Players"
            else:
                select_target = target

            selector = Select.From(select_target)
            super().__init__(selector, on_call)


    class PlaceThreatOn(Base):
        def __init__(self, value: int,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,) -> None:
            from game.card.card_finder import CardFinder

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                effect.this.PlaceThreatOnSchemes(targets, value, effect)
                return True

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                    ),
                )
            super().__init__(selector, on_call)

    class RemoveFromGame(Base):
        def __init__(self, target: 'Literal["This"]',
                    ) -> None:
            from game.operate.faces import Faces

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                return Faces.RemoveAllFromGame(targets, effect) == targets

            selector = Select.From(
                target,
            )
            super().__init__(selector, on_call)

    class RemoveFromCampaignLog(Base):
        def __init__(self, target: 'Literal["This"]',
                    ) -> None:
            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                return True

            selector = Select.From(
                target,
            )
            super().__init__(selector, on_call)

    class PutIntoPlay(Base):
        def __init__(self,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,
                    from_where: List['SELECT.WHERE']=["Default"],
                    ) -> None:
            from game.card.card_finder import CardFinder
            self.return_put_cards: List['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                for face in targets:
                    face.PutIntoPlay(player, effect)
                    self.return_put_cards = [face]
                    return True
                return False

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                    ),
                    from_where=from_where
                )
            super().__init__(selector, on_call)

    class ReturnToHand(Base):
        def __init__(self,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,
                    from_where: List['SELECT.WHERE']=["Default"],
                    # alliance: 'Selector|None'=None,
                    *,
                    to_who: Literal["Initiator", "Owner"]) -> None:
            from game.operate.faces import Faces
            from game.card.card_finder import CardFinder
            self.return_to_hand_cards: List['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if to_who == "Initiator":
                    if not player:
                        return False
                    faces = Faces.ReturnToHand(targets, player, effect)
                    self.return_to_hand_cards = faces
                    return faces == targets
                elif to_who == "Owner":
                    faces = Faces.ReturnToHand(targets, "Owner", effect)
                    self.return_to_hand_cards = faces
                    return faces == targets
                return False

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                    ),
                    from_where=from_where
                )
            # if selector.filter.finder.card_type == None:
            #     selector.filter.AddFinder(CardFinder(card_type=PlayerCard))
            super().__init__(selector, on_call)

    # CORRECTIF (pack brawn) : « Return this card to your reserve » en COUT.
    # Calque de ReturnToHand ci-dessus, seule la zone d'arrivee change. Utilise
    # par Silk bw002 (« Action: Return Silk to your reserve → ... »).
    class ReturnToReserve(Base):
        def __init__(self,
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,
                    from_where: List['SELECT.WHERE']=["Default"],
                    ) -> None:
            from game.card.card_finder import CardFinder
            self.returned_cards: List['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                faces = player.PutIntoReserve(targets, effect)
                self.returned_cards = list(faces)
                return list(faces) == list(targets)

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_type=card_type,
                    ),
                    from_where=from_where
                )
            super().__init__(selector, on_call)

    # "01018"
    class Discard(Base):
        def __init__(self, 
                    target: 'TARGET_TYPE|None'=None,
                    name: str|None=None,
                    trait: "CardFace.TRAITS|None"=None,
                    card_class: "ClassCard.CARD_CLASS|None"=None,
                    card_type: 'Type[TC]|Any|None'=None,
                    with_attach: 'CardFinder|bool|None'=None,
                    attach_to: 'CardFinder|None'=None,
                    has_printed_res: "Resources.RBYG|None"=None, # convert_green_res = False
                    combined_resource_cost: Tuple[int, int]|None=None,
                    highest_cost: bool=False,
                    check_effect: Callable[['Effect', 'TC'], bool]|None=None,
                    from_where: List['SELECT.WHERE']=["Default"],
                    range: 'SELECT.RANGE_TYPE'="Default",
                    ) -> None:
            from game.operate.faces import Faces
            from game.deck import Deck
            from game.card.face.card_face import CardFace
            from game.card.card_finder import CardFinder
            self.return_original_area: Dict[CardFace, Deck] = {}
            self.return_discarded_cards: List['CardFace'] = []

            # « discard N card(s) from your hand » : le cout accepte aussi une
            # carte glissee que sa carte hote rend defaussable « comme en main »
            # (td012 Donatello's Shell). Sans hote de ce genre en jeu, la liste
            # des cibles est exactement `YourHandCards` d'avant.
            if target == "YourHandCards":
                target = "YourHandCardsDiscardable"

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                # We need to do this before discard them
                self.return_original_area = {}
                for target in targets:
                    self.return_original_area[target] = target.card.area

                if Faces.DiscardAll(targets, effect) == targets:
                    self.return_discarded_cards = list(targets)
                    return True
                else:
                    return False

            # from_where: List['SELECT.WHERE']=["InPlay"]
            # random = False
            # bind_to: 'CardFinder|Literal["YourHero"]|CardFace|None'=None # for statues card

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(
                    target,
                    finder=CardFinder(
                        name=name,
                        trait=trait,
                        card_class=card_class,
                        card_type=card_type,
                        with_attach=with_attach,
                        attach_to=attach_to,
                        has_printed_res=has_printed_res,
                        canbe_discard=True,
                        check_effect_fn=check_effect
                    ),
                    combined_resource_cost=combined_resource_cost,
                    highest_cost=highest_cost,
                    # check_fn=check_fn,
                    from_where=from_where,
                    # bind_to=bind_to,
                    # random=random,
                    range=range,
                )
            super().__init__(selector, on_call)

        @override
        def OnEffectEnd(self, targets: Sequence['CardFace'], effect: 'Effect'):
            pass

    # "13027"
    class Spend(Base):
        def __init__(self, cost: 'Cost') -> None:
            self.return_res: 'Resources'

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                # We need to do this before discard them
                if not player:
                    return False
                spent_res = player.AskSpendResourcesInternal(cost, effect)
                if spent_res:
                    self.return_res = spent_res
                    return True
                else:
                    return False

            selector = Select.From("This")
            super().__init__(selector, on_call)

    class Counter(Base):
        def __init__(self,
                     target: 'TARGET_TYPE',
                     size: int|Literal["Damage"]|Tuple[int, int],
                     name: 'CardFace.COUNTER',
                     ):
            from game.card.face.attribute.can_place_counter import CanPlaceCounter
            # from game.operate.faces import Faces
            self.return_remove_counter: int = 0

            def has_enough_counter(effect: 'Effect', face: 'CardFace') -> bool:
                # TODO: Fix
                # if ability.when == Send.WhenPlayerPayingResources:
                #     # Fix "30004" vs "30001a"
                #     message = message.CastTo(Send.WhenPlayerPayingResources)
                #     cost_counter = message.for_effect.ability.cost_counter
                #     if cost_counter and cost_counter.GetThis(effect) == effect.this and name == cost_counter.name:
                #         num += cost_counter.num
                if isinstance(face, CanPlaceCounter):
                    if isinstance(size, tuple):
                        return face.GetCounters(name) >= size[0]
                    elif isinstance(size, int):
                        return face.GetCounters(name) >= size
                    elif size == "Damage":
                        return face.GetCounters(name) > 0
                return False

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                nonlocal size
                total_num = 0

                for target in targets:
                    result_num = 0
                    this = target.CastTo(CanPlaceCounter)
                    if isinstance(size, tuple):
                        min_size, max_size = size
                    elif isinstance(size, int):
                        max_size = size
                        min_size = max_size
                    elif size == "Damage":
                        assert isinstance(effect.bind_message, Message.WhenUnitWouldTakeDamage)
                        max_size = effect.bind_message.will_take_damage
                        min_size = max_size

                    if min_size != max_size:
                        max_size = min(max_size, this.GetCounters(name))
                        if not player:
                            return False
                        result_num = player.DeclareNumber(min_size, max_size)
                    else:
                        result_num = max_size

                    # if Faces.RemoveCountersOn([this], result_num, name, effect, forced=False) == None:
                    if this.RemoveCountersInternal(result_num, name, effect, forced=False) == None:
                        self.return_remove_counter = 0
                        return False
                    else:
                        total_num += result_num
                self.return_remove_counter = total_num
                return True

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(target)
            selector.selector_filter.AddParameter(check_effect_fn=has_enough_counter)
            super().__init__(selector, on_call)

    class PlaceCounter(Base):
        def __init__(self,
                     target: 'TARGET_TYPE',
                     num: int,
                     name: 'CardFace.COUNTER'):
            from game.operate.faces import Faces
            
            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                this = effect.this
                Unused(this)

                value = Faces.PlaceCountersOn(targets, num, name, effect) 
                if value == None:
                    return False
                return value >= num

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(target)
            super().__init__(selector, on_call)

    class PlaceTokens(Base):
        def __init__(self,
                     target: 'TARGET_TYPE',
                     num: int,
                     name: 'CardFace.TOKEN'):
            from game.operate.faces import Faces

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                value = Faces.PlaceTokensOn(targets, num, name, effect)
                if value == None:
                    return False
                return value >= num

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(target)
            super().__init__(selector, on_call)

    class RemoveTokens(Base):
        def __init__(self,
                     target: 'TARGET_TYPE',
                     size: int|Tuple[int, int],
                     name: 'CardFace.TOKEN'):
            from game.card.face.attribute.can_place_token import CanPlaceToken
            self.return_removed_tokens = 0

            def has_enough_counter(effect: 'Effect', face: 'CardFace') -> bool:
                if isinstance(face, CanPlaceToken):
                    if isinstance(size, tuple):
                        return face.GetTokens(name) >= size[0]
                    else:
                        return face.GetTokens(name) >= size
                return False

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                nonlocal size
                total_num = 0

                for target in targets:
                    result_num = 0
                    this = target.CastTo(CanPlaceToken)
                    if isinstance(size, tuple):
                        min_size, max_size = size
                    else:
                        max_size = size
                        min_size = max_size

                    if min_size != max_size:
                        max_size = min(max_size, this.GetTokens(name))
                        if not player:
                            return False
                        result_num = player.DeclareNumber(min_size, max_size)
                    else:
                        result_num = max_size

                    if this.RemoveTokensInternal(result_num, name, effect, forced=False) == None:
                        self.return_removed_tokens = 0
                        return False
                    else:
                        total_num += result_num
                self.return_removed_tokens = total_num
                return True

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(target)
            selector.selector_filter.AddParameter(check_effect_fn=has_enough_counter)
            super().__init__(selector, on_call)

    class RemoveEachCounter(Base):
        def __init__(self, target: 'TARGET_TYPE', name: 'CardFace.COUNTER') -> None:
            from game.card.face.attribute.can_place_counter import CanPlaceCounter
            from game.operate.faces import Faces
            self.return_remove_counter = 0

            def has_enough_counter(effect: 'Effect', face: 'CardFace') -> bool:
                if not isinstance(face, CanPlaceCounter):
                    return False
                return face.GetCounters(name) > 0

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                for target in targets:
                    this = target.CastTo(CanPlaceCounter)
                    value = Faces.RemoveCountersOn([this], "All", name, effect)
                    if value != None:
                        self.return_remove_counter = value
                return True

            if isinstance(target, Selector):
                selector = target
            else:
                selector = Select.From(target)
            selector.selector_filter.AddParameter(check_effect_fn=has_enough_counter)
            super().__init__(selector, on_call)

    class SearchForCard(Base):
        def __init__(self,
                     finder: 'CardFinder|Type[TC]',
                     do_what: Literal["PutIntoPlayEngagedYou", "Reveal"],
                     *,
                     include_encounter_deck: bool=False,
                     include_encounter_discard_pile: bool=False,
                     encounter_deck_top: int|None=None,
                     include_set_aside: bool=False,
                     range: 'SELECT.RANGE_TYPE'=(1, 1),
                     ):
            from game.card.card_finder import CardFinder
            from game.operate.search import Search
            self.searched_faces: List['CardFace'] = []

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                do_ok = False

                if isinstance(finder, CardFinder):
                    card_type = None
                    card_finder = finder
                else:
                    card_type = finder
                    card_finder = None

                if encounter_deck_top != None:
                    faces = Search.SearchForCards(
                        effect,
                        player,
                        include_encounter_deck=True,
                        finder=card_finder,
                        card_type=card_type,
                        range=range,
                        most_top=10
                    )

                else:
                    faces = Search.SearchForCards(
                        effect,
                        player,
                        include_encounter_deck=include_encounter_deck,
                        include_encounter_discard_pile=include_encounter_discard_pile,
                        include_set_aside=include_set_aside,
                        finder=card_finder,
                        card_type=card_type,
                        range=range
                    )

                for face in faces:
                    if do_what == "PutIntoPlayEngagedYou":
                        do_ok = face.PutIntoPlay(player, effect)
                    elif do_what == "Reveal":
                        do_ok = face.Reveal(player, effect) != None

                if do_ok:
                    self.searched_faces = faces

                return do_ok

            super().__init__(Select.From("This"), on_call)

    class DiscardDeckTopUntil(Base):
        def __init__(self,
                     which_deck: Literal["EncounterDeck", "YourDeck"],
                     card_type: 'Type[TC]',
                     do_what: Literal["PutIntoPlayEngagedYou", "Reveal", "PutIntoPlayUnderYourControl"]|None=None):
            from game.operate.worlds import Worlds
            self.return_discard_card: CardFace

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False

                if which_deck == "EncounterDeck":
                    face = Worlds.DiscardEncounterCardsUntil(effect, card_type=card_type)
                elif which_deck == "YourDeck":
                    face = player.DiscardDeckUntil(effect, card_type=card_type)

                if face:
                    self.return_discard_card = face
                    if do_what == None:
                        return True
                    elif do_what == "PutIntoPlayEngagedYou" or do_what == "PutIntoPlayUnderYourControl":
                        return face.PutIntoPlay(player, effect)
                    elif do_what == "Reveal":
                        """
                        you would be able to respond to Return the Favor with a card like Enhanced Spider-Sense and still deal the 5 damage.
                        The reason is, the “cost” to resolve Return the Favor’s 5 damage is to simply “reveal” the treachery; it does not necessitate the full resolution of that treachery.
                        Most hero cards will cancel “when revealed” effects on treacheries after the treachery card is revealed.
                        TODO: If there was a card out there that cancelled the “revealing” of a treachery card, then it would also cancel the 5 damage from Return the Favor.
                        NOTE: I don't think we can use "Enhanced Spider-Sense" to cancel it, it is from encounter discard pile, not from encounter deck
                        """
                        return face.Reveal(player, effect) != None
                    assert False, f"{do_what=}"
                return False

            super().__init__(Select.From("This"), on_call)

    class DiscardDeckTopCards(Base):
        def __init__(self,
                     which_deck: Literal["YourDeck", "EncounterDeck"],
                     size: int|Callable[[Effect], int]|Tuple[int, int]
                     ):
            self.return_discarded_cards: List[CardFace] = []
            from game.operate.worlds import Worlds

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False

                if isinstance(size, int):
                    max_size = size
                    min_size = size
                elif isinstance(size, tuple):
                    min_size, max_size = size
                else:
                    max_size = size(effect)
                    min_size = max_size

                if min_size != max_size:
                    select_size = player.DeclareNumber(1, max_size)
                else:
                    select_size = max_size

                if which_deck == "YourDeck":
                    # ⚠ DECK PLUS COURT QUE LE COUT (25/09/2026, signalements
                    # 21/22 de Yarro, arbitrage utilisateur). Rules Reference,
                    # Empty Player Deck : si le deck s'epuise pendant une
                    # defausse, on remelange, on prend 1 carte rencontre, et
                    # rien n'est defausse du nouveau deck. La defausse
                    # s'arrete donc la (`continue_after_shuffle=False`) et le
                    # cout est PAYE. Avant, il etait declare impaye : cartes
                    # perdues, effet jamais resolu (gb011-gb014, nv002,
                    # nv003, 04164...).
                    taille_avant = player.player_deck.GetSize()
                    discarded_cards = player.DiscardDeckTopCards(select_size, effect)
                    self.return_discarded_cards = discarded_cards
                    attendu = min(select_size, taille_avant)
                    return attendu > 0 and len(discarded_cards) == attendu
                else:
                    discarded_cards = Worlds.DiscardEncounterCards(select_size, effect)
                self.return_discarded_cards = discarded_cards
                return len(self.return_discarded_cards) == select_size

            super().__init__(Select.From("This"), on_call)

    class Rampage(Base):
        """AJOUT (16/10/2026) : mot-cle MAISON « Rampage X » des aspects TMNT (Inkwire).

        Texte de rappel imprime : « As an additional cost for this card, take X
        damage and discard X cards from the top of your deck. » Fiche :
        docs/reference/mots-cles/rampage.md (huit evenements FERAL, dont ua015).

        UN seul cout qui COMPOSE les deux couts existants, dans l'ordre imprime,
        pour heriter de leurs regles deja arbitrees au lieu de les recopier :
          1. `TakeDamage(X, "YourIdentity")` : l'identite (heros OU alter-ego)
             subit X degats ; des degats EMPECHES (Tough...) = cout impaye
             (Rules Reference, « Cost »), un payeur qui en meurt a PAYE.
          2. `DiscardDeckTopCards("YourDeck", X)` : un deck plus court que X
             s'epuise, se remelange, rien de plus n'est defausse, et le cout est
             PAYE (arbitrage utilisateur du 25/09/2026, Rules Reference
             « Player Deck »). Seuls un deck ET une defausse vides le rendent
             impayable.
        Les cartes defaussees : `effect.cost_func.Get(CostFunc.Rampage)
        .return_discarded_cards`.

        ⚠ « Cannot pay all of the costs → pay none » (Rules Reference, « Cost ») :
        la partie DEFAUSSE se verifie AVANT de prendre les degats, et des la
        question « jouable ? » (selecteur), sinon un deck vide ferait perdre X PV
        pour rien. « Deck vide » = `DiscardDeckTopCards` refuse (`attendu > 0`) ;
        en partie, un deck ne reste vide que si la defausse l'est aussi (il se
        remelange aussitot, Rules Reference « Player Deck »).
        """
        def __init__(self, x: int) -> None:
            from game.card.card_finder import CardFinder
            assert isinstance(x, int) and x > 0, f"Rampage {x!r}"
            self.x = x
            self.return_discarded_cards: List[CardFace] = []
            degats = CostFunc.TakeDamage(x, "YourIdentity")
            defausse = CostFunc.DiscardDeckTopCards("YourDeck", x)

            def peut_defausser(effect: 'Effect', face: 'CardFace') -> bool:
                joueur = effect.GetInitiator()
                if joueur is None:
                    return False
                return joueur.player_deck.GetSize() > 0

            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                self.return_discarded_cards = []
                if not player or degats.call_fn == None or defausse.call_fn == None:
                    return False
                if player.player_deck.GetSize() == 0:
                    return False
                if not degats.call_fn(targets, effect, player):
                    return False
                paye = defausse.call_fn([], effect, player)
                self.return_discarded_cards = list(defausse.return_discarded_cards)
                return paye

            selector = Select.From("YourIdentity", finder=CardFinder(check_effect_fn=peut_defausser))
            selector.selector_filter.AddParameter(has_non_health=False)
            super().__init__(selector, on_call)

    # Will ignore "Requirement"
    class PayPrintCost(Base):
        def __init__(self, res: Literal["Target"]):
            from game.card.face.attribute.has_cost import HasCost
            from game.element.resources import Resources
            self.return_paid_resources: Resources = Resources("0")

            # We cannot use dynamic cost because of "01072"
            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if not player:
                    return False
                if res == "Target":
                    that_ally = effect.targets[0].CastTo(HasCost)
                    # If that ally’s aspect matches that of The Power of [Aspect] card, then The Power of [Aspect] card will generate 2 resources. However, if that ally’s aspect does not match, The Power of [Aspect] card will only generate 1 resource.
                    paid_res = player.PayCardPrintCost(that_ally, effect)
                else:
                    paid_res = player.AskSpendResourcesInternal(res, effect)
                if paid_res != None:
                    self.return_paid_resources = paid_res
                    return True
                return False

            super().__init__(Select.From("This"), on_call)

    class RemoveThreatFrom(Base):
        def __init__(self,
                     target: 'TARGET_TYPE|None',
                     value: int,
                     *,
                     ignore_crisis: bool=False,
                     ):
            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                this = effect.this
                removed = this.RemoveThreatFromSchemes(targets, value, effect, ignore_crisis=ignore_crisis)
                return removed != None and removed > 0

            if isinstance(target, Selector):
                target = target
            else:
                target = Select.From(target)
            super().__init__(target, on_call)

    class TuckCardHere(Base):
        def __init__(self,
                target: 'TARGET_TYPE|None',
                *,
                must_from_encounter_discard_pile: bool=False,
                ):

            self.tucked_cards: List['CardFace'] = []
            def on_call(targets: Sequence['CardFace'], effect: 'Effect', player: 'Player|None') -> bool:
                if must_from_encounter_discard_pile:
                    for target in targets:
                        if not target.card.area.flags.is_encounter_discard_pile:
                            return False

                this = effect.this
                self.tucked_cards = list(targets)
                return this.TuckCardUnderHere(targets, effect)

            if isinstance(target, Selector):
                target = target
            else:
                target = Select.From(target)
            super().__init__(target, on_call)

