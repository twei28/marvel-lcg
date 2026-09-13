from core import *
from game.card.face import *
from game.deck import *
from game.ability import *
from game.ability.factory import *
from game.message import *
from game.player import *
from cards.paper import Paper

@final
# CORRECTIF (12/09/2026, pack `sentinel`) : `CanAttach` ajoute a la liste.
# `st010` Juston Seyfert est un SOUTIEN qui dit « Action: Attach to a side
# scheme » ; le moteur ne savait attacher que les Asset2 (ameliorations et
# attachements). L'ajout est INERTE pour les 300 soutiens existants : tous les
# points d'entree de `CanAttach` commencent par tester `self.bind_face`, qui
# reste None tant qu'aucune carte n'appelle `AttachTo2`.
class Support(CanAttach, HasUses, HasPermanent, HasSetup, ClassCard, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def GetAbilities(self) -> List['Ability']:
        abilities: List['Ability'] = []
        if not self.ability.Find(func_name="Play"):
            abilities.append(
                AbilityFactory.CanPlayThisSupportCard()
            )
        return abilities + super().GetAbilities()

    @override
    def OnPutIntoPlay(self, message: 'Message.WhenCardPutIntoPlay') -> 'bool':
        from game.operate.faces import Faces
        if Faces.MoveAllTo([self], message.GetToPlayer().supports, message.by_effect):
            return super().OnPutIntoPlay(message)
        else:
            return False

    @override
    def OnWouldEnterPlay(self, into_area: 'Deck') -> bool:
        if super().OnWouldEnterPlay(into_area):
            if self.HasTrait("TEAM"):
                if into_area.GetOwner().IsPlayer():
                    player = into_area.GetOwnerPlayer()
                    if not player.limit_team.CheckLimit([self]):
                        return False
            return True
        return False

    @property
    @override
    def bind_face(self) -> 'CardFace|None':
        # CORRECTIF (12/09/2026, pack `sentinel`) : un soutien ATTACHE vit dans
        # la zone d'ameliorations de sa cible, pas dans celle d'un joueur.
        # `GetOwner()` n'y rend alors aucun joueur, et `bind_face` valait None
        # alors que la carte etait bel et bien accrochee — `st010` Juston
        # Seyfert, « Action: Attach to a side scheme », plantait sur l'assertion
        # de `GetBindFace()`. On repasse la main a `CanAttach` dans ce seul cas.
        # Inerte pour les soutiens ordinaires : aucun d'eux n'entre jamais dans
        # une zone d'ameliorations.
        if self.card.area.flags.is_upgrades:
            return super().bind_face
        player = self.card.area.GetOwner()
        if isinstance(player, Player):
            return player.GetIdentity()
        return None

