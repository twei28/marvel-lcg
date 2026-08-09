from cards.pack import *

# ---------------------------------------------------------------------------
# « Marvelous » — logique commune aux deux faces de Stan Lee.
#
# Stan Lee n'a aucune carte signature : son deck contient 15 cartes signature
# EMPRUNTEES a d'autres heros. La carte dit qu'il « a les boites de texte » de
# ces heros. Le moteur ne sait pas copier une boite de texte arbitraire, mais il
# sait faire « compter comme » : on lui prete donc les NOMS des heros concernes
# (consider_as). Toutes les cartes signature qui verifient le nom du heros
# (« attachez a X », « si X est votre identite »...) fonctionnent alors.
# ---------------------------------------------------------------------------


def NomPropre(nom: str) -> str:
    """Retire le marqueur d'unicite eventuel (« * Peter Parker »)."""
    return str(nom).lstrip("* ").strip()


def TrouverJoueur(this: 'CardFace') -> 'Player|None':
    world = this.card.world
    for pl in world.players:
        if not Player.IsType(pl):
            continue
        if this in pl.GetAllIdentityFace():
            return pl
    return None


def SetsEmpruntes(player: 'Player') -> List[str]:
    """Sets de heros representes par les cartes du joueur, hors le notre."""
    sets: List[str] = []
    for deck in (player.player_deck, player.hand_cards, player.discard_pile):
        for face in deck.Get():
            set_name = face.paper.set_name
            if not set_name or set_name == "Stan Lee":
                continue
            if set_name not in sets:
                sets.append(set_name)
    return sets


def NomsAPreter(player: 'Player') -> List[str]:
    """Noms d'identite (heros et alter-ego) des sets empruntes."""
    from cards.database import CardsDB

    noms: List[str] = []
    for set_name in SetsEmpruntes(player):
        for card_id in CardsDB.sets_cards.get(set_name, []):
            paper = CardsDB.papers.get(card_id)
            if paper is None or paper.type not in ("Hero", "AlterEgo"):
                continue
            nom = NomPropre(paper.name)
            if nom and nom != "Stan Lee" and nom not in noms:
                noms.append(nom)
    return noms


def AppliquerMarvelous(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
    """Prete a toutes les identites de Stan Lee les noms des heros empruntes.

    Idempotent : les deux faces portent l'aptitude, la premiere qui se declenche
    fait le travail, la seconde ne double rien.
    """
    this = effect.this
    player = TrouverJoueur(this)
    if player is None:
        return

    noms = NomsAPreter(player)
    if not noms:
        return

    for face in player.GetAllIdentityFace():
        for nom in noms:
            if nom in face.consider_as.names:
                continue
            face.SetConsiderAs(face, 1, name=nom)


def MarvelousAbilities() -> Sequence['Ability']:
    """Marvelous doit etre (re)applique a la mise en place ET a chaque bascule.

    Changer de forme reinitialise le modele de la carte (`OnResetModel` appelle
    `ResetConsiderAs`) : sans la seconde aptitude, Stan Lee perdrait tous les
    noms empruntes en passant en forme heros — soit des le premier tour.
    """
    return [
        AbilityFactory.AfterGameSetup(AppliquerMarvelous),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Rule,
            "You",
            lambda effect, message: AppliquerMarvelous(effect, message),
        ).SetName("Marvelous"),
    ]
