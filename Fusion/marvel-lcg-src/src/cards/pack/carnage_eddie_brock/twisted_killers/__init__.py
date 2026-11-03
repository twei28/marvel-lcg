from cards.pack import *

# ===========================================================================
# Set modulaire « Twisted Killers » (ca019-ca023). Helpers partages ICI (lecon hk005).
# ===========================================================================
NOM_MURDEROUS_NATURE = "Murderous Nature"


def PersonnagesAmisEnJeu(effect: 'Effect', joueur: 'Player|None' = None) -> List['CardFace']:
    """Personnages « amis » en jeu : l'identite et les allies du joueur (ou de tous les joueurs si `joueur` est None)."""
    cartes: List['CardFace'] = []
    for face in Worlds.GetOnFieldCards(effect):
        if not face.IsInPlay():
            continue
        if not (Hero.IsType(face) or AlterEgo.IsType(face) or Ally.IsType(face)):
            continue
        if joueur is not None and face.GetControlByPlayer() is not joueur:
            continue
        cartes.append(face)
    return cartes


def PlusFaibleEnPV(candidats: Sequence['CardFace']) -> List['CardFace']:
    """Les cartes de PV RESTANTS minimal (ex aequo : toutes, le joueur departage)."""
    if not candidats:
        return []
    mini = min(f.health for f in candidats)
    return [f for f in candidats if f.health == mini]
