from cards.pack import *

# ===========================================================================
# Pack HAWKEYE (Kate Bishop) — contenu custom de CptScorp, reproduit a
# l'identique (Marvel Champions Custom Project, Cycle 2).
#
# Kate est un quasi-clonage de Hawkeye (Clint Barton, cf. core/01066 et
# wonder_man/58013) : la mecanique centrale est le compteur "arrow" sur
# l'upgrade unique « Kate's Bow ». Contrairement a l'ally officiel (qui
# depense TOUJOURS 1 compteur pour un effet fixe), Kate's Bow accumule tout
# seul 1 compteur par fin de phase joueur (jusqu'a 10), et « Master Archer »
# (kb001a, l'identite elle-meme) en depense un nombre VARIABLE choisi par le
# joueur (0 a 3, ou 0 a 5 avec Kate's Quiver) pour degats.
#
# `NOM_ARC` / `NOM_CARQUOIS` : les deux seuls noms de carte cherches par
# plusieurs fichiers a la fois (Master Archer et Kate's Quiver visent tous
# deux Kate's Bow ; Kate's Quiver et Tandem Archery le nomment aussi). Centraliser
# le nom evite une faute de frappe silencieuse repetee dans 6 fichiers.
# ===========================================================================

NOM_ARC = "Kate's Bow"
NOM_CARQUOIS = "Kate's Quiver"


def TrouverArcEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Kate's Bow s'il est EN JEU (sous le controle du joueur), sinon None."""
    return Worlds.FindCardOnField(effect, name=NOM_ARC)


def PlacerCompteursFlecheSurArc(effect: 'Effect', nombre: int) -> None:
    """Place `nombre` compteurs 'arrow' sur Kate's Bow (plafond 10), si en jeu.

    Utilise par toutes les cartes qui « placent des compteurs sur Kate's Bow » :
    l'ally Hawkeye (kb002), Quick Draw (kb005), Lucky (kb009), Kate's Quiver
    (kb013), Tandem Archery (kb015), et Kate's Bow lui-meme en fin de phase.
    """
    if nombre <= 0:
        return
    arc = TrouverArcEnJeu(effect)
    if arc is None:
        return
    Faces.PlaceCountersOn([arc], nombre, 'arrow', effect, maximum=10)
