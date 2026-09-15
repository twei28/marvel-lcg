from game.card.face.base import *
from game.card.face import *
from game.ability import *
from game.message import *
from game.player import *
from cards.paper import Paper

class SchemeSide2(HasAccelerationIcon, Scheme2):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def OnPutIntoPlay(self, message: 'Message.WhenCardPutIntoPlay') -> 'bool':
        from game.operate.faces import Faces
        world = self.card.world
        if self.card.area == world.area_schemes_side or \
            Faces.MoveAllTo([self], world.area_schemes_side, message.by_effect, target_game_area=message.target_game_area):
            entree = super().OnPutIntoPlay(message)
            # ⚠ LA PORTE UNIQUE DES DEUX TYPES DE MANIGANCE ANNEXE, etablie par
            # trace le 15/09/2026 : la mise en place de Klaw y passe
            # (`01116a.py` -> `SetupCards.Reveal` -> `Reveal` -> `PutIntoPlay`),
            # et une annexe posee en cours de partie aussi.
            #
            # ⚠ APRES l'entree, pas avant : le panneau du plateau MONTRE la
            # carte, elle doit deja etre sur la table. `ConfirmSideSchemeReveal`
            # ne retient que ce que le SCENARIO impose et ne fait rien sans son
            # drapeau de regle.
            if entree:
                world.ConfirmSideSchemeReveal(self)
            return entree
        else:
            return False

    def IgnoreKeywordUntilRoundEnd(self, by_effect: 'Effect', *keywords: 'CardFace.IGNORE_KEY'):
        for keyword in keywords:
            self.SetIgnoreKeyword(+1, keyword, by_effect)

        from cards.pack import RunAt
        def action():
            for keyword in keywords:
                self.SetIgnoreKeyword(-1, keyword, by_effect)
        RunAt.RoundEnd(by_effect, action)

