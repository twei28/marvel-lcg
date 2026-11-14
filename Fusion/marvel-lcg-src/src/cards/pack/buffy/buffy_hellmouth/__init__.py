from cards.pack import *
# Helpers partages du set (⚠ un helper du __init__ du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).

def Trouver(effect: 'Effect', joueur: 'Player', nom: str, card_type: Any=CardFace) -> 'CardFace|None':
    """« find X » (Rules Reference v1.8, fiche `mots-cles/find.md`) : deck rencontre, defausse rencontre ET zone de mise de cote."""
    return Search.SearchForCard(
        effect,
        joueur,
        include_encounter_deck=True,
        include_encounter_discard_pile=True,
        include_set_aside=True,
        name=nom,
        card_type=card_type,
    )


def JoueurDeLaDefaite(effect: 'Effect', message: Any) -> 'Player':
    """Le joueur qui a vaincu la carte ; a defaut le premier joueur."""
    try:
        return message.GetDefeatingPlayer()
    except Exception:
        return Worlds.GetFirstPlayer(effect)


def ChoisirUnJoueur(effect: 'Effect', joueur: 'Player') -> 'Player':
    """« under any player's control » : seul en partie, on prend le joueur ; a plusieurs il choisit parmi les identites."""
    joueurs = list(Worlds.GetPlayers(effect))
    if len(joueurs) <= 1:
        return joueur
    identites = [j.GetIdentity() for j in joueurs]
    choix = joueur.AskChooseFace(identites, effect, prompt="Choose a player", forced=True)
    return choix.GetControlByPlayer() if choix is not None else joueur

NOM_BECOMING = "Becoming"
NOM_ENEMIES_ALIGNED = "Enemies Aligned"
NOM_FAITH = "Faith"
NOM_ANGELUS = "Angelus"
NOM_ANGEL = "Angel"
NOM_SCYTHE = "Slayer Scythe"
NOM_CHOSEN_ONE = "Chosen One"
NOM_PROPHECY_GIRL = "Prophecy Girl"
