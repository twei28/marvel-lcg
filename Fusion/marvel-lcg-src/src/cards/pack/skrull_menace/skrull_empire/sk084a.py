from . import *

# Further Empire Expansion 3A — complot principal, face A (2A, 3A, 4A) : « When Revealed: Discard cards from
# the encounter deck until a SKRULL minion is discarded. Put that minion into
# play engaged with the first player. »
#
# Carte de reference : **`01116b`** Underground Distribution —
# `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` puis
# `face.PutIntoPlay(premier_joueur, effect)`. Ici le filtre ajoute le trait
# SKRULL (helper `SbireSkrullDuDeckRencontre`).
#
# ⚠ Mots-pieges : « a SKRULL minion » (trait ET type) ; « engaged with the
# FIRST player » ; le sbire est MIS EN JEU (pas revele : ses When Revealed ne
# partent pas). Deck rencontre epuise : la regle native remelange la defausse
# et pose un jeton d'acceleration (FAQ du livret p. 20, A New Skrull Is Born).


def GetAbilities() -> Sequence['Ability']:

    def sbire(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        face = SbireSkrullDuDeckRencontre(effect)
        if face is not None:
            face.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, sbire),
    ]
