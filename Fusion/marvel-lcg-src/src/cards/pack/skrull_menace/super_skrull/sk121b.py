from . import *

# Heir to the Throne 2B — complot principal, face B (derniere : « If this stage
# is completed, the players lose the game », regle native du dernier stade).
# When Revealed: Reveal the top card of the SUPERPOWER deck.
#
# Carte de reference : **`skrull_empire/sk085b`** (derniere face B du scenario 1,
# meme texte de defaite) et `sk120b` (ce set).
#
# ⚠ Mots-pieges : « Reveal » (une seule carte) ; valeurs de menace (12 par
# joueur, depart 2 par joueur, escalade +2 par joueur) dans desc, lues sur
# l'image.


def GetAbilities() -> Sequence['Ability']:

    def superpouvoir(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        RevelerSuperpouvoir(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, superpouvoir),
    ]
