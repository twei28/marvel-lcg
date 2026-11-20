from . import *

class Rand:

    @staticmethod
    def IsDisableShuffle(effect: 'Effect|World') -> 'bool':
        from game.world import World
        if isinstance(effect, World):
            world = effect
        else:
            world = effect.world
        return world.rule.disable_shuffle

    T = TypeVar("T")
    @staticmethod
    def RandomChoice(input_list: Sequence[T], effect: 'Effect|World') -> T:
        assert input_list != []
        if Rand.IsDisableShuffle(effect):
            return input_list[0]
        return Random.RandomChoice(input_list)

    @staticmethod
    def RandomChoice2(input_list: Sequence[T], x: int, effect: 'Effect|World') -> List[T]:
        if Rand.IsDisableShuffle(effect):
            return [input_list[0]]
        return Random.RandomChoice2(input_list, x)

    @staticmethod
    def RandomCards(faces: 'Sequence[CardFace]', size: int, effect: 'Effect|World', player: 'Player|None'=None) -> 'List[CardFace]':
        """`RandomChoice2` pour des CARTES CACHEES (main, paquet, zone de cote).

        Regle de partie `tirage_manuel` allumee : le joueur designe lui-meme les cartes parmi des dos melanges
        (`Player.AskPickHiddenCard`). Sinon, ou pour des cartes deja sur la table (rien de cache a melanger),
        c'est le tirage du moteur, inchange. (Case cochee = le joueur l'a voulu : meme en graine 0.)"""
        from game.world import World
        world = effect if isinstance(effect, World) else effect.world
        if not world.rule.tirage_manuel.val or len(faces) <= size or any(face.card.IsOnField() for face in faces):
            return Rand.RandomChoice2(faces, size, effect)
        joueur = player or world.GetCurrentPlayer()
        restantes = list(faces)
        choisies: 'List[CardFace]' = []
        for _ in range(size):
            choisie = joueur.AskPickHiddenCard(restantes)
            choisies.append(choisie)
            restantes.remove(choisie)
        return choisies

    @staticmethod
    def Shuffle(list: List[Any], effect: 'Effect') -> None:
        if Rand.IsDisableShuffle(effect):
            return
        return Random.Shuffle(list)

