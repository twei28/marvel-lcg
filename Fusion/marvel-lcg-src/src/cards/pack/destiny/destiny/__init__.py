from cards.pack import *
# Helpers partages du set « Destiny » (⚠ un helper defini dans le `__init__.py` du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
NOM_GLIMPSE = "Glimpse of the Future"
NOM_MYSTIQUE = "Mystique"
NOM_RAVEN = "Raven Darkhölme"


def GlimpseDe(joueur: 'Player') -> 'CardFace|None':
    """Glimpse of the Future (dy002) du joueur : amelioration PERMANENTE posee a la mise en place, jamais retiree du jeu."""
    glimpse = joueur.GetControlUpgrade(CardFinder(name=NOM_GLIMPSE))
    return glimpse[0] if glimpse else None


def CartesSousGlimpse(joueur: 'Player') -> List['CardFace']:
    """« the card tucked under Glimpse of the Future » : la zone des cartes glissees sous l'amelioration."""
    glimpse = GlimpseDe(joueur)
    return list(glimpse.GetPlacedCardArea().Get()) if glimpse is not None else []


def IconesSousGlimpse(joueur: 'Player') -> int:
    """X = « the number of icons ([star] and [boost]) on the card tucked under Glimpse of the Future ».

    ⚠ `CountTotalBoostStarAndBoost` et NON `CountTotalBoostIcons` (qui ne somme que les icones chiffrees, pas l'etoile) : lecon sn014."""
    pile = CartesSousGlimpse(joueur)
    return FacesCounter.CountTotalBoostStarAndBoost(pile) if pile else 0


def ChoisirDistincts(effect: 'Effect', joueur: 'Player', candidats: Sequence['CardFace'], combien: int, invite: str) -> List['CardFace']:
    """« for each resource spent this way, choose a DIFFERENT scheme/enemy » : autant de cibles distinctes que de ressources, plafonnees au nombre de candidats."""
    k = min(combien, len(candidats))
    if k <= 0:
        return []
    return joueur.AskChooseFaces(list(candidats), (k, k), effect, prompt=invite, peek=True, not_move=True)
