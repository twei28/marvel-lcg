from cards.pack import *
# Helpers partages du set « RoboCop Nemesis » (⚠ un helper du __init__ du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
NOM_ED_209 = "ED-209"
NOM_STAIRS = "Stairs"
NOMS_ROBOCOP = ("RoboCop", "Alex Murphy")


def JoueurRoboCop(effect: 'Effect') -> 'Player|None':
    """« the RoboCop player » : le joueur dont l'identite est RoboCop / Alex Murphy (a defaut, None)."""
    for joueur in Worlds.GetPlayers(effect):
        identite = joueur.GetIdentity()
        if identite is not None and any(identite.IsName(nom, check_all_face=True) for nom in NOMS_ROBOCOP):
            return joueur
    return None


def Trouver(effect: 'Effect', joueur: 'Player', nom: str, card_type: Any=CardFace) -> 'CardFace|None':
    """« find X » (fiche `mots-cles/find.md`) : deck rencontre, defausse rencontre ET zone de mise de cote (nemesis compris)."""
    return Search.SearchForCard(
        effect,
        joueur,
        include_encounter_deck=True,
        include_encounter_discard_pile=True,
        include_set_aside=True,
        name=nom,
        card_type=card_type,
    )
