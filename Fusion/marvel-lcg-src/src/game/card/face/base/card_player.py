from typing import TypeAlias
from core import *
from game.card.face.base import *
from game.card.face import *
from game.deck import *
from game.ability import *
from game.ability.factory import *
from game.message import *
from game.player import *
from cards.paper import Paper
from game.element.resources import Resources

class PlayerCard(CanSurge, CanAccelerationToken, CardFace):
    pass

class ClassCard(HasResourceIcon, HasCost, HasMaxPer, PlayerCard):

    ASPECT_CLASS_TYPE: TypeAlias = Literal[
        'Aggression',   # red
        'Justice',      # yellow
        'Leadership',   # blue
        'Protection',   # green
        "'Pool",
        # CORRECTIF (divergence volontaire) : le cinquieme aspect, fan-made.
        # FFG l'avait concu puis abandonne, dispersant ses cartes dans les
        # quatre autres ; designhacker.ca l'a repris. CARD_CLASS_LIST et
        # ASPECT_CLASS_LIST sont DERIVEES de ces Literal (Types.LiteralToList
        # dans game/element/utility.py), donc les declarer ici suffit a la
        # validation, au typage et a la construction de deck.
        'Determination',  # purple
        # CORRECTIF (divergence volontaire) : le SIXIEME aspect, fan-made lui
        # aussi. « Venomized » (ekAugust) fait jouer n'importe quel heros comme
        # s'il etait lie a un symbiote. Meme chemin que Determination : ces deux
        # `Literal` suffisent, CARD_CLASS_LIST et ASPECT_CLASS_LIST en sont
        # DERIVEES (Types.LiteralToList, game/element/utility.py).
        'Venomized',      # black
    ]

    CARD_CLASS: TypeAlias = Literal[
        "Aggression",   # red
        "Justice",      # yellow
        "Leadership",   # blue
        "Protection",   # green
        "'Pool",        # pink
        "Determination",  # purple - CORRECTIF, voir ASPECT_CLASS_TYPE
        "Venomized",      # black  - CORRECTIF, voir ASPECT_CLASS_TYPE
        "Basic",
        "IdentitySpecific",
        "Encounter",    # e.g. "04097"
        "Campaign",
        "Aspect",       # Non-Hero Non-basic card, non-basic
    ]

    DECK_BUILDING_CLASS: TypeAlias = Literal[
        "Cyclops",
        "Domino"
    ]

    @override
    def __init__(self, paper: 'Paper') -> None:
        self.max_per_deck = 3
        self.card_classes: List["ClassCard.CARD_CLASS"] = []
        self.classification: "ClassCard.CARD_CLASS"
        # Permanent cards are set aside at the start of step 1 of setup
        super().__init__(paper)

        self.RegisterAttribute("MaxPerDeck", "max_per_deck")
        self.RegisterAttribute("UnitCost", None)

        def parse(value: str):
            from game.element.utility import IsCardClass, IsAspectClass
            self.card_classes = []
            card_classes = value.split(";")
            for card_class in card_classes:
                if card_class == "Hero":
                    card_class = "IdentitySpecific"
                assert IsCardClass(card_class)
                self.card_classes.append(card_class)
            for card_class in self.card_classes:
                if IsAspectClass(card_class):
                    self.card_classes.append("Aspect")
                    break
        self.RegisterAttribute("Class", parse)

    @override
    def GetAbilities(self) -> List['Ability']:
        abilities: List['Ability'] = []

        # Generate resource in play
        resources_abilities = self.ability.Find(func_name="CanGenerateResources")
        assert len(resources_abilities) <= 1
        if resources_abilities and not self.ability.Find(func_name="DoGenerateResources"):
            abilities.append(AbilityFactory.DoGenerateResources(
                resources_abilities[0].second_type, # This function is for select, so it cannot be like a Temp
                "This",
                ex_operation=resources_abilities[0].generate_resources_ex_operation
            ))

        # Resources
        if not self.ability.Find(func_name="CheckThisCanDropPay"):
            abilities.append(
                AbilityFactory.CheckThisCanDropPay(
                ),
            )
        # Drop pay
        if not self.ability.Find(func_name="DiscardPay"):
            abilities.append(
                # Discard this to pay
                AbilityFactory.DoDiscardThisToGenerateResources(
                    AbilityType.DiscardForResource,
                )
            )

        return abilities + super().GetAbilities()

    @override
    def CheckPrintedValue(self):
        assert self.card_classes != [], f"{self.paper.card_id=}"
        return super().CheckPrintedValue()

    def OnAfterPlay(self, player: 'Player', by_effect: 'Effect', play_message: 'Message.WhenPlayerPlayCard', message: 'Message2', from_area: 'Deck'):
        from game.message import Message
        played_message = Message.AfterPlayerPlayedCard(player, self, by_effect, play_message, message, from_area)
        played_message.Send()
        by_effect.world.stat.RecordPlayedCard(player, self)

    ################################################################################
    # Should we remove `player`? we had have the owner
    def Play(self, player: 'Player', by_effect: 'Effect', message: 'Message2', resource: 'Resources', from_area: 'Deck', is_like_from_hand: bool) -> bool:
        from game.message import Message
        from game.operate.faces import Faces

        # We do this at `ResolveEffect`
        # Faces.MoveAllToProcessingArea([self], by_effect)
        assert self.card.area.flags.is_processing
        by_effect.context.paid_this_resources = resource
        by_effect.this.CastTo(HasCost).SetPaidResources(resource)
        # assert self.card.face.GetPlayer() == player, f"{self.card.face} {player=}"
        assert by_effect.GetInitiator() == player, f"{self.card.face} {player=}"

        if not by_effect.ProcessSelfCost():
            # ⚠ LE JUMEAU DE `PlayerAction.ResolveEffect` (correctif du
            # 20/09/2026, signalement Yarro n°18). Meme situation, meme regle :
            # une mise en jeu qui echoue n'a pas eu lieu, la carte retourne
            # d'ou elle vient au lieu d'etre defaussee. Ici c'est le cout
            # PROPRE de la carte qui n'a pas pu etre paye, les ressources
            # l'ayant deja ete. `from_area` est le PARAMETRE de cette methode,
            # toujours renseigne -- pas `context.play_from_area`, qui est vide
            # sur les mises en jeu gratuites et forcerait une branche de repli.
            Faces.MoveAllTo([self], from_area, by_effect)
            return False

        would_play_message = Message.WhenPlayerWouldPlayCard(player, by_effect, resource, from_area, is_like_from_hand)
        would_play_message.Send()

        def discard():
            # "40032" doesn't make the discard, so we have to try to discard it here.
            if self.IsInProcessingArea():
                Faces.DiscardAll([self], by_effect)

        if not would_play_message.is_be_instead:
            play_message = Message.WhenPlayerPlayCard(player, would_play_message)
            play_message.Send()
            if would_play_message.be_cancel:
                # Will be discarded in `OnAfterPlay`
                # discard()
                pass
            else:
                by_effect.ResolveSelf(message, by_effect, to_player=player, skip_cost=True)
            self.OnAfterPlay(player, by_effect, play_message, message, from_area)
            return True
        else:
            discard()
            return False

    def IsClass(self, * card_classes: "ClassCard.CARD_CLASS") -> bool:
        for card_class in self.card_classes:
            if card_class in card_classes:
                return True
        return False
            # or \
            # self.consider_as.IsConsiderAs(card_class=card_class)

    def IsDeckBuildingClass(self, deck_building_class: "ClassCard.DECK_BUILDING_CLASS") -> bool:
        if not self.IsClass("IdentitySpecific"):
            return False
        if self.paper.set_name != deck_building_class:
            return False
        return True

    def GetAspect(self) -> 'ClassCard.ASPECT_CLASS_TYPE|None':
        from game.element.utility import IsAspectClass
        for card_class in self.card_classes:
            if IsAspectClass(card_class):
                return card_class
        return None

