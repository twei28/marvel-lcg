from core import *
from game.card.face import *
from game.ability import *
from game.message import *
from game.player import *
from cards.paper import Paper

@final
# CORRECTIF (18/09/2026, pack officiel Fear No Evil, set Disasters 60177-60179) :
# un environnement peut porter une icone de crise (Mystic Incursion, Sinking
# Ferry, Towering Inferno). Sans `CanCrisis`, `InitPrintedValue("Crisis")`
# tombait sur KeyError des la creation du deck rencontre.
class Environment(CanCrisis, HasAccelerationIcon, HasAmplify, HasHazard, HasUses, CanHinder, HasThreatLevel, CanPlaceCounter, HasPermanent, HasSetup, EncounterNonVillainCard, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def OnPutIntoPlay(self, message: 'Message.WhenCardPutIntoPlay') -> 'bool':
        # When a player reveals a Spell environment, they place that card in front of them in their play area. 
        from game.operate.faces import Faces
        if self.HasTrait("SPELL"):
            area_environment = message.GetToPlayer().area_environment
        else:
            area_environment = self.card.world.area_environment
        if Faces.MoveAllTo([self], area_environment, message.by_effect):
            return super().OnPutIntoPlay(message)
        else:
            return False

    @override
    def OnWhenCardRevealed(self, revealed_message: 'Message.WhenCardRevealed') -> None:
        player = revealed_message.GetToPlayer()
        # Fix "21100a" flip
        if revealed_message.is_by_flipping or \
            self.PutIntoPlay(player, revealed_message.by_effect):
            return super().OnWhenCardRevealed(revealed_message)

    @property
    def bind_face(self) -> 'CardFace|None':
        player = self.card.area.play_area
        if player:
            return player.GetIdentity()
        return None

    # AJOUT (15/10/2026, pack custom skrull_menace, scenario Skrull Empire) :
    # un environnement qui porte un CADRAN DE PV. « The villains in this
    # scenario do not have a hit point dial. Instead, the Skrull Empire
    # environment has a hit point dial » (livret p. 8). Un environnement n'a pas
    # d'attribut HP dans le moteur (HasHealth exige des PV imprimes sur chaque
    # carte : l'ajouter a la classe ferait tomber tous les environnements du
    # jeu). Les degats vivent donc en compteurs 'damage' (precedent 21100a
    # Avengers Tower), et la carte qui le veut DECLARE son cadran par script :
    #     face.cadran_pv = lambda: (pv_restants, pv_max)
    # Seule cette carte publie alors `health` / `max_health` / `cadran_pv`
    # vers le plateau, qui dessine la pastille et la jauge de PV comme pour un
    # personnage (card-model.ts). Aucun autre environnement n'est touche.
    cadran_pv: 'Callable[[], Tuple[int, int]]|None' = None

    @override
    def GetInfoDict(self) -> Dict[str, int]:
        info = super().GetInfoDict()
        if self.cadran_pv is not None:
            restants, maximum = self.cadran_pv()
            info |= {'cadran_pv': 1, 'health': int(restants), 'max_health': int(maximum)}
        return info

