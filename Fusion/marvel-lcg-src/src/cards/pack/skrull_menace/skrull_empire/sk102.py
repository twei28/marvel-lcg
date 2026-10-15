from . import *

# A New Skrull Is Born — TRAITRISE x2 (Skrull Empire). 1 boost.
# When Revealed: Discard cards from the encounter deck until you discard a
#   SKRULL minion and reveal it.
#
# Carte de reference : **`01116b`** (`Worlds.DiscardEncounterCardsUntil`) ; ici
# le sbire est REVELE (`face.Reveal(joueur, effect)`), donc ses When Revealed
# partent. FAQ du livret p. 20 : sans sbire SKRULL, la defausse est remelangee
# et un jeton d'acceleration posee : comportement natif du deck rencontre.


def GetAbilities() -> Sequence['Ability']:

    def naissance(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        face = SbireSkrullDuDeckRencontre(effect)
        if face is not None:
            face.Reveal(message.GetToPlayer(), effect)

    return [AbilityFactory.WhenThisRevealed(None, naissance)]
