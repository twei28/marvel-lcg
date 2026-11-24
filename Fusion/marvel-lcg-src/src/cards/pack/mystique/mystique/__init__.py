from cards.pack import *
# Helpers partages du set « Mystique » (⚠ un helper defini dans le `__init__.py` du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
#
# LES FORMES METAMORPHES (my003 Civilian, my004 Enemy, my005 Friend) sont des ameliorations a DEUX faces : la face `a` est la face VISIBLE (capacites actives),
# la face `b` la face CACHEE (meme texte imprime, grisee, aucune capacite). « Flip » = `card.Flip` (les deux faces s'echangent).
NOM_MYSTIQUE = "Mystique"
NOM_RAVEN = "Raven Darkhölme"
NOM_SHAPESHIFTER = "Shapeshifter"
NOM_DESTINY = "Destiny"
ID_CIVILIAN = "my003"
ID_ENEMY = "my004"
ID_FRIEND = "my005"
IDS_FORMES = (ID_CIVILIAN, ID_ENEMY, ID_FRIEND)


def IdDe(face: 'CardFace') -> str:
    return str(getattr(face.paper, "card_id", ""))


def EstUneForme(face: 'CardFace') -> bool:
    """« a shapeshift form upgrade » : l'une des trois ameliorations Civilian / Enemy / Friend (face visible OU cachee)."""
    return IdDe(face)[:5] in IDS_FORMES


def EstVisible(face: 'CardFace') -> bool:
    """La forme est FACE VISIBLE : sa face `a` est la face courante de la carte."""
    return EstUneForme(face) and IdDe(face).endswith("a")


def Formes(joueur: 'Player') -> List['CardFace']:
    """Les formes metamorphes en jeu sous le controle du joueur (les trois, visibles ou cachees)."""
    return [f for f in joueur.GetControlUpgrade() if EstUneForme(f)]


def FormeVisible(joueur: 'Player', id_forme: str) -> bool:
    """« the <Civilian/Enemy/Friend> shapeshift form upgrade is faceup »."""
    return any(IdDe(f).startswith(id_forme) and EstVisible(f) for f in Formes(joueur))


def ToutesCachees(joueur: 'Player') -> bool:
    formes = Formes(joueur)
    return bool(formes) and not any(EstVisible(f) for f in formes)


def Retourner(face: 'CardFace', effect: 'Effect') -> None:
    """« flip that card » : la face visible passe cachee et inversement."""
    face.card.Flip(effect)


def RetournerVisible(face: 'CardFace', effect: 'Effect') -> None:
    """« flip that card faceup » : sans effet si elle l'est deja."""
    if not EstVisible(face):
        face.card.Flip(effect)


def RetournerCachee(face: 'CardFace', effect: 'Effect') -> None:
    """« flip that card facedown » : sans effet si elle l'est deja."""
    if EstVisible(face):
        face.card.Flip(effect)


def EnJeuNomme(effect: 'Effect', *noms: str) -> List['CardFace']:
    """Les personnages (identite ou allie) en jeu portant l'un de ces noms."""
    return [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if any(f.IsName(n) for n in noms)]


def InfiltrationEnVitrine(effect: 'Effect', message: Any) -> bool:
    """« While Infiltration (my007) is in the victory display » : la carte vit en vitrine, donc la capacite est posee sur l'IDENTITE (RECETTES §3bis)."""
    Unused(message)
    return any(IdDe(f) == "my007" for f in Worlds.VictoryDisplay(effect).GetAll())


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un assert quand l'initiateur n'est pas un joueur, et le moteur AVALE l'exception
    (lecon `Player.GetHero()`, pack lady_sif). Meme helper que ares, sunfire, throg (un helper se recopie dans le set : il n'est pas partage entre packs).
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return None


def Degats(face: 'CardFace') -> int:
    """Les degats portes par un personnage : PV max - PV courants (le moteur n'a pas d'attribut `damage`)."""
    return int(face.max_health - face.health)
