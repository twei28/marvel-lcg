from core import *
from game.card.face import *
from game.ability import *
from game.message import *
from game.player import *
from cards.paper import Paper

@final
class EncounterSideScheme(SchemeSide2, CanCrisis, HasSetup, HasPermanent, EncounterNonVillainCard, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def OnBeDefeated(self, would_defeated_message: 'Message.WhenSchemeWouldBeDefeated|Message.WhenUnitWouldBeDefeated', *, as_asset: bool, ignore_when_defeated: bool):
        if self.permanent:
            # CORRECTIF (18/09/2026, 60113a Establish Trust, pack fne) : un
            # complot Permanent ne quitte pas le jeu, mais il EST vaincu : son
            # « When Defeated » (retourner la carte, jeton sur Disturbed Psyche)
            # ne partait jamais, le moteur sautait tout. On envoie les memes
            # messages que le cas general, sans la defausse.
            defeated_message = Message.WhenSchemeBeDefeated(self, would_defeated_message, ignore_when_defeated)
            defeated_message.Send()
            after_defeated_message = Message.AfterSchemeBeDefeated(self, would_defeated_message.by_effect, defeated_message)
            after_defeated_message.Send()
        else:
            return super().OnBeDefeated(would_defeated_message, as_asset=as_asset, ignore_when_defeated=ignore_when_defeated)

