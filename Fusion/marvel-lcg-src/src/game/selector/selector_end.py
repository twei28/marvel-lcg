from typing import Final
from core import *
from game.card.face import *
from game.effect import *
from game.deck import *

class SelectorEnd:
    def __init__(self,
                # Process rule
                peek: bool=False,
                not_move: bool=False,
                not_shuffle: bool=False,
                ):
        self.peek       = peek
        self.not_move   = not_move
        self.not_shuffle: Final = not_shuffle

    def Process(self, effect: 'Effect', targets: Sequence['CardFace']) -> bool:
        # Shuffle
        do_move = True
        if self.not_move:
            do_move = False
        if not self.not_shuffle:
            SelectorEnd.DoShuffle(effect, targets, do_move, False)
        elif do_move:
            SelectorEnd.DoMove(effect, targets, do_move)
        return True

    def OnSelectTargetFailure(self, effect: 'Effect', peeked_faces: Sequence['CardFace']) -> None:
        if self.peek and peeked_faces:
            SelectorEnd.DoShuffle(effect, peeked_faces, False, True)

    @staticmethod
    def DoMove(effect: 'Effect', faces: Sequence['CardFace'], need_move: bool) -> List['Deck']:
        from game.operate.faces import Faces

        places: List[Deck] = []
        moved_faces: List['CardFace'] = []

        for face in faces:
            deck = face.card.area
            if deck.flags.is_deck:
                if not face.card.IsFaceUp():
                    moved_faces.append(face)
                    places.append(face.card.area)

        if need_move:
            if moved_faces:
                # ⚠ C'EST ICI QU'UNE RECHERCHE SORT LA CARTE DU DECK, et le
                # SAS de recherche part de la (correctif du 21/09/2026,
                # signalement Aghenatak). Ce n'est PAS ici qu'on le NOTE :
                # `SelectorEnd` est appele avec l'effet jetable que
                # `AskChooseSelect` fabrique pour poser la question, pas avec
                # l'effet de la CARTE qui a lance la recherche. C'est
                # `SearchInternal.SearchForCardsInternal` qui note, sur
                # `by_effect`, et `EffectInvoker.CloseSearchTransit` qui
                # referme. Voir le commentaire de cette methode.
                Faces.MoveAllToProcessingArea(moved_faces, effect)
        else:
            # if moved_faces:
            #     CardFace.PeekCards(moved_faces, effect)
            pass

        return places

    @staticmethod
    def DoShuffle(effect: 'Effect', faces: Sequence['CardFace'], need_move: bool, is_failure: bool) -> None:
        from game.deck.deck import Deck

        places: List[Deck] = SelectorEnd.DoMove(effect, faces, need_move)

        if need_move or is_failure:
            for deck in Types.RemoveDuplicates(places):
                # ⚠ CORRECTIF DU 09/09/2026 — UN `assert deck.GetSize() != 0`
                # SE TROUVAIT ICI, ET IL RENDAIT INATTEIGNABLE LA BRANCHE
                # ECRITE JUSTE EN DESSOUS. L'auteur avait bien prevu le deck
                # vide (« if deck.GetSize() == 0: pass », on ne melange pas ce
                # qui n'existe plus) ; le garde de debogage au-dessus faisait
                # tomber le moteur avant d'y arriver.
                #
                # Ce n'est pas theorique : toute RECHERCHE qui sort la ou les
                # dernieres cartes du deck laisse ce deck a zero. En partie
                # RELEASE les assertions sont desactivees, le defaut restait
                # donc invisible ; sous le harnais de test elles sont actives,
                # et la capacite plantait en silence — le journal montrait
                # « was defeated » puis plus rien, et les cartes cherchees
                # DISPARAISSAIENT de toutes les zones.
                #
                # Trouve en portant `vz024` In the Thick of It, et reproduit a
                # l'identique sur la carte OFFICIELLE `40019` Lock and Load :
                # ce sont les DEUX qui etaient intestables, pas la carte
                # fan-made. Voir tools/test_capacites.py, cas « vz024 » et
                # « 40019 ».
                if deck.GetSize() == 0:
                    # Send.AfterDeckRunOut(deck)
                    # deck.ShuffleWithDiscardPile(True, effect)
                    pass
                else:
                    deck.Shuffle(effect)

