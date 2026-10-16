from core import *
from game.card.face import *
from game.deck import *
from game.ability import *
from game.message import *
from game.player import *
from cards.paper import Paper

@final
# AJOUT (16/10/2026, pack `jennika`, decision de l'utilisateur) : le type
# imprime PATH (« la Voie »), celui de `tj011` Sosaiken. Une Voie est une carte
# PERMANENTE mise en jeu par un Setup, jamais jouee depuis la main : pas de
# capacite `Play`, pas de limite d'equipe, pas d'attachement.
#
# Zone : l'AIRE DE SOUTIEN du joueur (`player.supports`) — aucune zone, aucun
# descripteur ni aucune colonne de plateau de plus. Le type Path n'est pas un
# Support (`Support.IsType` est faux) ; `Worlds.GetOnFieldSupports` et
# `GetControlCardsByType(support=True)` filtrent desormais sur le type : un
# effet qui vise « un soutien » ne voit donc pas la Voie.
class Path(HasUses, HasPermanent, ClassCard, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def OnPutIntoPlay(self, message: 'Message.WhenCardPutIntoPlay') -> 'bool':
        from game.operate.faces import Faces
        if Faces.MoveAllTo([self], message.GetToPlayer().supports, message.by_effect):
            return super().OnPutIntoPlay(message)
        else:
            return False

    @property
    @override
    def bind_face(self) -> 'CardFace|None':
        player = self.card.area.GetOwner()
        if isinstance(player, Player):
            return player.GetIdentity()
        return None
