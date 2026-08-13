from . import *

class AbilityTokenFactory:

    @staticmethod
    def AfterCardPlacedToken(ability_type: 'AbilityType',
                             which_card: CardType,
                             token_name: 'CardFace.TOKEN|None',
                             operation: OperationType[Message.AfterCardPlacedToken],
                             *,
                             conditions: ConditionsType[Message.AfterCardPlacedToken]=[],
                             at_least: Callable[['Effect'], int]|int|Literal["4*"]|None=None,
                             ) -> 'Ability':
        from game.operate.worlds import Worlds

        def check_which_card(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> bool:
            return Condition.CheckWhichCard(which_card, message.trigger, effect)

        def check_token_name(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> bool:
            if token_name:
                return message.token_name == token_name
            return True

        def check_at_least(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> bool:
            from game.card.face.attribute.can_place_token import CanPlaceToken
            if at_least:
                this = effect.this.CastTo(CanPlaceToken)
                if isinstance(at_least, str):
                    size = Worlds.ConvertPerPlayerIconToInt(at_least, effect)
                elif isinstance(at_least, int):
                    size = at_least
                else:
                    size = at_least(effect)
                assert token_name != None
                return this.GetTokens(token_name) >= size
            return True

        return Ability(
            ability_type,
            Message.AfterCardPlacedToken,
            [
                Condition2.ThisIsTrigger,
                check_which_card,
                check_token_name,
                check_at_least,
                *conditions
            ],
            operation,
            is_local=which_card == "This"
        )

    @staticmethod
    def WhenCardWouldBePlacedToken(ability_type: 'AbilityType',
                                    to_where: CardType,
                                    counter_name: 'CardFace.TOKEN|None',
                                    operation: OperationType[Message.WhenCardWouldBePlacedToken],
                                    *,
                                    conditions: ConditionsType[Message.WhenCardWouldBePlacedToken]=[],
                                    ) -> 'Ability':

        def check_to_where(effect: 'Effect', message: Message.WhenCardWouldBePlacedToken) -> bool:
            return Condition.CheckWhichCard(to_where, message.trigger, effect)

        def check_counter_name(effect: 'Effect', message: Message.WhenCardWouldBePlacedToken) -> bool:
            if counter_name:
                return message.token_name == counter_name
            return True

        return Ability(
            ability_type,
            Message.WhenCardWouldBePlacedToken,
            [
                check_to_where,
                check_counter_name,
                *conditions
            ],
            operation,
            is_local=to_where == "This"
        )

    @staticmethod
    def WhenCardWouldRemovedToken(ability_type: 'AbilityType',
                                  from_where: CardType,
                                  token_name: 'CardFace.TOKEN|None',
                                  operation: OperationType[Message.WhenCardWouldRemovedToken],
                                  *,
                                  conditions: ConditionsType[Message.WhenCardWouldRemovedToken]=[],
                                  ) -> 'Ability':
        """La fenetre « quand on RETIRERAIT des jetons d'ici ».

        Le pendant de `WhenCardWouldBePlacedToken`, qui existait seul. Le
        message, lui, existait deja et porte tout ce qu'il faut : `would_remove`
        (le nombre), `remove_all`, et `is_be_instead` pour remplacer le retrait
        par autre chose.

        Ecrit pour le complot principal de The Spot, dont le texte deroute la
        menace au lieu de la retirer : « When you would remove any amount of
        threat from here [...], move that threat to the card with the highest
        Threat Level instead. »
        """

        def check_from_where(effect: 'Effect', message: Message.WhenCardWouldRemovedToken) -> bool:
            return Condition.CheckWhichCard(from_where, message.trigger, effect)

        def check_token_name(effect: 'Effect', message: Message.WhenCardWouldRemovedToken) -> bool:
            if token_name:
                return message.token_name == token_name
            return True

        return Ability(
            ability_type,
            Message.WhenCardWouldRemovedToken,
            [
                check_from_where,
                check_token_name,
                *conditions
            ],
            operation,
            is_local=from_where == "This"
        )
