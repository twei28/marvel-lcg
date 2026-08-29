from core import *
from game.card.face import *
from game.deck import *
from game.ability import *
from game.message import *
from game.player import *
from cards.paper import Paper
from game.element.damage_property import DamageProperty

@final
# CORRECTIF (29/08/2026) : `CanPlaceCounter` ajoute.
# Un evenement ne sejourne normalement pas en jeu, il n'avait donc jamais eu
# besoin de porter des compteurs. Le pack custom `dazzler` est le premier cas :
# ses evenements [[SONG]] RESTENT dans la « Setlist » de Live Concert, et la
# carte du heros dit mot pour mot « place 1 sound counter ON A SONG in the
# Setlist ». Le compteur doit donc vivre sur la chanson, pas ailleurs.
#
# C'est une addition PUREMENT d'API, sans etat nouveau : le composant qui
# stocke les compteurs (`components.counter`) est deja cree pour TOUTE carte
# par `Card.Components.__init__` (game/card/card.py:97), et le moteur le
# commente lui-meme : « We create all of components here for card change ».
# Le mixin n'ouvre que l'acces (`GetCounters`, `PlaceCountersInternal`,
# `RemoveCountersInternal`) et le rendu (`GetInfoDict` -> cle `c_<nom>`).
#
# LIMITE D'AFFICHAGE, mesuree et independante de ce correctif : la Setlist est
# batie sur la `PlaceCardArea`, declaree `is_out_of_play = True`
# (game/deck/deck_type.py:34). `GetRenderInfo` (card_face.py:369) n'emet donc
# rien pour ces cartes, compteur compris. Le jeton EXISTE bien sur la bonne
# carte et le journal l'annonce, mais aucun badge ne s'affiche dessus.
class Event(HasTeamUp, HasAlliance, ClassCard, CanPlaceCounter, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def OnAfterPlay(self, player: 'Player', by_effect: 'Effect', play_message: 'Message.WhenPlayerPlayCard', message: 'Message2', from_area: 'Deck'):
        from game.operate.faces import Faces
        if self.IsInProcessingArea():
            Faces.DiscardAll([self], by_effect)
        super().OnAfterPlay(player, by_effect, play_message, message, from_area)

    @override
    def OnDealDamage(self, units: List['Unit2'], damage: 'int|DamageProperty', by_effect: 'Effect', *, property: 'AttackProperty|None'=None, attack_in_event: bool) -> int|None:
        assert self == by_effect.this, f"{self=} {by_effect.this=}"
        # Fix "48018"
        identity = by_effect.GetInitiator().GetIdentity()
        if identity.IsDefeated():
            return None
        return identity.OnDealDamage(units, damage, by_effect, property=property, attack_in_event=attack_in_event)

    @override
    def OnRemoveSchemeThreat(self, schemes: List['Scheme2'], value: int, by_effect: 'Effect') -> int|None:
        assert by_effect != None, f"{self=}"
        assert self == by_effect.this, f"{self=} {by_effect.this=}"
        identity = by_effect.GetInitiator().GetIdentity()
        return identity.OnRemoveSchemeThreat(schemes, value, by_effect)

