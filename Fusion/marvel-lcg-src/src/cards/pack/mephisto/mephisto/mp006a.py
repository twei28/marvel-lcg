from . import *

# Complot principal Hellbound Obsession (3A). When Revealed: Shuffle each BARGAIN attachment from the encounter discard pile into the encounter deck.
# Flip the Gateway to Corruption environment to reveal the Hell environment.
#
# Cartes de reference : sm/venom/27079 (`card.Flip(effect)` sur un environnement a deux faces), `PactsDeLaDefausseDansLeDeck` (set).
# ⚠ Mots-pieges : FLIP (le meme objet, face Hell) et non « defausser puis reveler » ; si Gateway n'est pas en jeu il n'y a rien a retourner.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        PactsDeLaDefausseDansLeDeck(effect)
        passerelle = PasserelleOuEnfer(effect)
        if passerelle is not None and getattr(passerelle.paper, "card_id", None) == "mp007a":
            passerelle.card.Flip(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
