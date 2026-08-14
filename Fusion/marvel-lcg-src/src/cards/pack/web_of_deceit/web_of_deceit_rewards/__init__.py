from cards.pack.web_of_deceit import *

# Les 50 cartes des cinq arbres de talents. Elles sont JOUEUR, pas rencontre :
# le carnet de campagne les pose dans le deck de leur proprietaire a chaque mise
# en place (voir `campaign.py`), et le joueur les joue comme les siennes.


def ChercherEtPrendreEnMain(effect: 'Effect', joueur: 'Player', **finder) -> 'CardFace|None':
    """« Search your deck and discard pile for X and add it to your hand. »"""
    trouvee = Search.SearchForCard(
        effect,
        joueur,
        include_player_deck=True,
        include_player_discard_pile=True,
        **finder
    )
    if trouvee:
        Faces.AddToHand([trouvee], joueur, effect)
    return trouvee


# Les dix cartes de l'arbre Symbiosis, que « Get it Off! » compte dans la pile
# de victoire. Le set_name ne suffit pas : les cinq arbres le partagent.
SYMBIOSIS = ["wd%03d" % n for n in range(142, 152)]
