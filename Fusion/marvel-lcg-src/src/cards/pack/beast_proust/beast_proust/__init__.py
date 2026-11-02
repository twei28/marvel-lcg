from cards.pack import *
# Helpers partages du set « Beast Proust » (⚠ un helper defini dans le `__init__.py` du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
NOM_LAB = "Beast's Lab"
PLAFOND_LAB = 3


def LabDe(joueur: 'Player') -> 'CardFace|None':
    """Beast's Lab (bs002) du joueur : soutien PERMANENT mis en jeu a la mise en place."""
    labs = [f for f in joueur.supports.Get() if f.IsName(NOM_LAB)]
    return labs[0] if labs else None


def GlisseesSousLab(joueur: 'Player') -> List['CardFace']:
    """« the cards tucked under Beast's Lab » : la zone des cartes glissees sous le soutien."""
    lab = LabDe(joueur)
    return list(lab.GetPlacedCardArea().Get()) if lab is not None else []


def LabPret(joueur: 'Player') -> bool:
    """Beast's Lab en jeu ET redresse : on peut l'incliner en cout."""
    lab = LabDe(joueur)
    return lab is not None and lab.CanExhaust()


def CoutImprime(face: 'CardFace') -> int:
    """« the printed cost of this card » : `printed_cost.val` (pas le cout paye) ; 0 pour une carte sans cout imprime (ressource...)."""
    cout = getattr(face, "printed_cost", None)
    return int(cout.val) if cout is not None else 0


def AmeliorationsTech(joueur: 'Player') -> List['CardFace']:
    """« a TECH upgrade you control » : amelioration portant le trait TECH, sous le controle du joueur (allies compris)."""
    return [f for f in joueur.GetControlUpgrade() if f.HasTrait("TECH")]


def Glisser(joueur: 'Player', faces: 'CardFace|Sequence[CardFace]', effect: 'Effect') -> bool:
    """Glisse des cartes sous Beast's Lab, VISIBLES de tous (on doit les voir pour les jouer). Le plafond de 3 est une Reponse forcee du Lab (bs002)."""
    lab = LabDe(joueur)
    return lab is not None and lab.TuckCardUnderHere(faces, effect, peek=True)


def ChercherTechEtGlisser(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    """« search your deck or discard pile for a TECH upgrade, then tuck it under Beast's Lab » (Tech Support, Tech Genius). La recherche melange le deck."""
    face = Search.PlayerCard(
        effect,
        joueur,
        include_player_deck=True,
        include_discard_pile=True,
        trait="TECH",
        card_type=Upgrade,
    )
    if face is not None:
        Glisser(joueur, face, effect)
    return face
