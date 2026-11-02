from . import *

# Dimensional Portal (module Darkhold). Traitrise SPELL, SPELL OF DARKHOLD. « When Revealed : If Darkhold is attached to the villain, discard cards
# from the top of the encounter deck until a minion, reveal that minion, and remove 1 darkspell counter from Darkhold. Otherwise, find Darkhold and
# reveal it. » Cartes de reference : trors/zola `TheMadDoctor` (`Worlds.DiscardEncounterCardsUntil(card_type=Minion)`), `ResolutionDeSort`.
# Le sbire defausse puis REVELE s'engage avec le joueur et resout ses « When Revealed » (`face.Reveal(joueur)`).


def GetAbilities() -> Sequence['Ability']:
    def sort(effect: 'Effect', joueur: 'Player') -> None:
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is not None:
            sbire.Reveal(joueur, effect)

    return [ResolutionDeSort(sort)]
