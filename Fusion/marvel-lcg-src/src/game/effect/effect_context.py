from core import *
from game.card.face import *
from game.effect import *
from game.message import *
from game.player import *
from game.world import *
from game.element.resources import Resources
from game.element.cost import Cost

@final
class EffectContext:

    def __init__(self, effect: 'Effect') -> None:
        self.effect = effect
        self.end_attack_messages: List['Message.AfterUnitAttackEnd'] = []
        self.end_thwart_messages: List['Message.AfterUnitThwartEnd'] = []
        self.initialized_targets: List[bool] = []
        self.paid_this_cost: 'Cost' = Cost("0")
        self.paid_this_resources: 'Resources' = Resources("0")
        self.targets_internal: List['CardFace'] = []

        self.bind_message: 'Message2|None' = None # 'self.ability.when', can only set None once, for "45078"

        self.is_must_choose = False
        self.only_work_when_no_other_options = False

        self.target_range: Tuple[int, int] = (0, 0)
        self.all_legal_targets: List['CardFace'] = []
        self.ignore_resource_cost: bool = False
        self.ask_player: 'Player|None' = None

        self.this_effect_need_cost: 'Cost|None' = None
        self.paid_this_res_effects: List['Effect'] = []

        # CORRECTIF (pack brawn) : zone d'ou part la carte jouee. Le moteur la
        # deplace en zone de traitement AVANT de faire payer, si bien qu'au
        # moment du paiement plus rien ne dit d'ou elle venait. La Reserve en a
        # besoin : une carte jouee depuis la main ne se finance que par la main.
        self.play_from_area: 'Deck|None' = None

        # CORRECTIF (21/09/2026, signalement Aghenatak) : le SAS de recherche.
        # Chaque paire dit « cette carte est sortie de ce deck vers la zone de
        # traitement pendant cet effet ». `SearchInternal.SearchForCardsInternal`
        # REMPLIT la liste, `EffectInvoker.CloseSearchTransit` la vide a la fin
        # de la resolution et renvoie chez elle toute carte que personne n'a
        # reclamee. Sans cela une carte cherchee mais non consommee restait
        # posee sur la table pour toujours, ni en jeu ni en defausse
        # (61008, 61019, 62022).
        #
        # ⚠ LE REMPLISSEUR N'EST PAS `SelectorEnd.DoMove`, MEME SI C'EST LUI
        # QUI DEPLACE LA CARTE. `SelectorEnd` est appele avec l'effet JETABLE
        # que `AskChooseSelect` fabrique pour poser la question, lequel se
        # resout — et donc se refermerait — des que le joueur a repondu, avant
        # que l'operation appelante ait pu consommer la carte. C'est
        # exactement le geste qui a casse `ze014` The Mother of Night le
        # 21/09/2026. Le sas se note sur le `by_effect` de la CARTE qui
        # cherche, et nulle part ailleurs.
        self.search_transit: List[Tuple['CardFace', 'Deck']] = []

        # Spell effect
        self.initiator: User = self.effect.this.GetControlByOrOwner()

    def AddAtkMessage(self, end_message: 'Message.AfterUnitAttackEnd'):
        self.end_attack_messages.append(end_message)

    def AddThwMessage(self, end_message: 'Message.AfterUnitThwartEnd'):
        self.end_thwart_messages.append(end_message)

    def ResetBeforeOperation(self):
        self.end_attack_messages = []
        self.end_thwart_messages = []
        self.initialized_targets = [False, False, False]

    def GetTargetsInternal(self, index: int) -> List['CardFace']:
        assert index != 0
        assert self.initialized_targets[index] == False
        effect = self.effect
        initiator = effect.GetInitiator()
        # Fix "18004"
        labels: List['Ability.LABEL'] = [x for x in effect.ability.labels if x != 'defense']
        selector = effect.ability.selectors[index]
        self.initialized_targets[index] = True
        if selector != None:
            return initiator.AskChooseSelect(selector, effect, labels=labels, for_second_target=True)
        else:
            return []

    def ResetBeforeCondition(self):
        self.is_must_choose = False
        self.only_work_when_no_other_options = False

    def ResetAfterOperation(self):
        # Before effect
        self.target_range = (0, 0)
        self.all_legal_targets = []
        self.ignore_resource_cost: bool = False
        self.ask_player: 'Player|None' = None

        self.this_effect_need_cost: 'Cost|None' = None
        self.paid_this_res_effects: List['Effect'] = []

        self.play_from_area: 'Deck|None' = None # CORRECTIF (pack brawn)

        self.initiator: User = self.effect.this.GetControlByOrOwner()

        self.targets_internal: List['CardFace']

