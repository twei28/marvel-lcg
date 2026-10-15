from cards.pack import *

# ===========================================================================
# Helpers PARTAGES par les sets modulaires de Skrull Menace livres ensemble :
# Shaper of Worlds, les cinq ensembles d'ELITES (Crusader, Jazinda, Skymax,
# War Skrull, Xavin) et les alternatives Standard Skrull / Expert Skrull
# (sk228-sk262). Chaque `__init__.py` de set fait
# `from cards.pack.skrull_menace.communs_modulaires import *`.
#
# Les Elites sont des SBIRES « Elite » uniques (Victory 1) : chaque ensemble de
# six cartes se compose du sbire, d'un attachement (ou deux), d'un complot
# annexe, d'une ou deux traitrises. Plusieurs attachements disent « Attach to a
# SKRULL minion. If you cannot, attach to the villain. » : une seule regle,
# `AttacherAUnSbireSkrull`.
# ===========================================================================


def LeMechant(effect: 'Effect') -> 'Villain|None':
    """« The villain » : le mechant en jeu (premier de la zone si plusieurs)."""
    return Worlds.FindVillain(effect)


def DonnerBoostAuMechant(effect: 'Effect', nombre: int = 1) -> int:
    """« Give the villain N facedown boost card(s). » Rend le nombre donne (0 sans mechant)."""
    mechant = LeMechant(effect)
    if mechant is None or nombre <= 0:
        return 0
    Faces.GiveFacedownBoostCards([mechant], nombre, effect)
    return nombre


def AttacherAUnSbireSkrull() -> 'Ability':
    """« Attach to a SKRULL minion. If you cannot, attach to the villain. » Modele 01100 / sk146
    (`AttachToFaceWhenPutIntoPlay` + `otherwise_attach_to`) : le joueur qui revele choisit parmi les
    sbires SKRULL en jeu (un seul : sans question) ; aucun : le mechant."""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(
        CardFinder(card_type=Minion, trait="SKRULL"),
        otherwise_attach_to=Villain,
    )


def EnnemisSkrull(effect: 'Effect') -> List['CardFace']:
    """« each SKRULL enemy » : sbires ET mechant porteurs du trait SKRULL, en jeu."""
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Enemy.IsType(f) and f.IsInPlay() and f.HasTrait("SKRULL")]


def SbiresSkrull(effect: 'Effect') -> List['CardFace']:
    return [f for f in EnnemisSkrull(effect) if Minion.IsType(f)]


def MettreEnJeuEngage(effect: 'Effect', face: 'CardFace', joueur: 'Player') -> bool:
    """« Put <face> into play engaged with you » : un sbire mis en jeu s'engage avec le joueur
    (aucun « When Revealed » ne part). Rend vrai si la carte est en jeu ensuite."""
    face.PutIntoPlay(joueur, effect)
    return face.IsInPlay()
