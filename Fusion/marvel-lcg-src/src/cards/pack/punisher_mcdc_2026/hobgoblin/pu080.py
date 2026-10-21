from . import *

# Guise to Terrorize — TRAITRISE x2. Boost 2.
# When Revealed : Discard a card from the encounter deck. If the discarded card is a treachery, resolve the "Pumpkin
#   Bomb" ability. Otherwise, reveal that card.
#
# Cartes de reference : `Worlds.DiscardEncounterCards(1, effect)`, `face.Reveal(joueur, effect)` (an015, 27099).
#
# ⚠ « reveal THAT card » : la carte qu'on vient de defausser, qui quitte la defausse pour etre revelee (sbire : entre
# en jeu engage ; complot annexe : entre en jeu...) ; deck vide = rien.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        cartes = Worlds.DiscardEncounterCards(1, effect)
        if not cartes:
            return
        carte = cartes[0]
        if Treachery.IsType(carte):
            ResoudrePumpkinBomb(effect, joueur, 1)
        else:
            carte.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
