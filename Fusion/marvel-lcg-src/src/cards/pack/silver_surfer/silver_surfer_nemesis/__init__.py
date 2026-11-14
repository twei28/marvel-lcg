from cards.pack import *

# Helpers partages du set « Silver Surfer Nemesis ».

NOM_GALACTUS = "Galactus"
NOM_MANGEUR = "The World Eater"


def ChercherEnRencontre(effect: 'Effect', nom: str, card_type: Any=None) -> 'CardFace|None':
    """Cherche une carte nommee dans le deck de rencontre ou sa defausse (« Reveal The World Eater »).

    ⚠ `Search` sort la carte du deck (sas de traitement) : l'appelant DOIT la consommer (mise en jeu...).
    """
    joueur = effect.GetInitiator() if Player.IsType(getattr(effect, "initiator", None)) else None
    if joueur is None:
        joueur = Worlds.GetCurrentPlayer(effect)
    faces = Search.SearchForCards(
        effect, joueur,
        include_encounter_deck=True,
        include_encounter_discard_pile=True,
        name=nom,
        card_type=card_type,
    )
    return faces[0] if faces else None
