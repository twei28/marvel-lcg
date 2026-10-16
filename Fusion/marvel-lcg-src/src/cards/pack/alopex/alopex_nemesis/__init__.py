from cards.pack import *

# Helpers partages du set « Alopex Nemesis » (Inkwire, TMNT Heroes, prefixe `ta`).
# ⚠ L'obligation `ta012` Manipulated a le bandeau « ALOPEX », pas
# « ALOPEX NEMESIS » : son module vit dans `alopex/alopex/`.


def DefausserUneCarteDeLaMain(joueur: 'Player', effect: 'Effect') -> bool:
    """« Discard 1 card from your hand. » — le JOUEUR choisit (pas au hasard).

    Modele `raphael_nemesis/__init__.py` (57062). Rend True si une carte a ete
    defaussee, False si la main est vide.
    """
    main = list(joueur.hand_cards.Get())
    if not main:
        return False

    def defausser(choisies: Sequence['CardFace']) -> None:
        Faces.DiscardAll(list(choisies), effect)

    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Discard 1 card from your hand",
            defausser,
        ).SetTarget(main, range=(1, 1), not_move=True),
    )
    return True
