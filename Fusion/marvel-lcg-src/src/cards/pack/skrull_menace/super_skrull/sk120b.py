from . import *

# Searching for the Heir 1B — complot principal, face B.
# When Revealed: Reveal the top card of the SUPERPOWER deck.
#
# Carte de reference : **`skrull_empire/sk082b`** (When Revealed qui revele la
# carte du dessus d'un paquet de scenario, `RevelerPlanete`) ; ici
# `RevelerSuperpouvoir` (helper du set).
#
# ⚠ Mots-pieges : « Reveal » (l'attachement entre en jeu et s'attache au
# Super-Skrull, il n'est pas « mis en jeu » a la main) ; une seule carte ; paquet
# vide : rien. Valeurs de menace (6 par joueur, depart 0, escalade +1 par
# joueur) dans desc, lues sur l'image.


def GetAbilities() -> Sequence['Ability']:

    def superpouvoir(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        RevelerSuperpouvoir(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, superpouvoir),
    ]
