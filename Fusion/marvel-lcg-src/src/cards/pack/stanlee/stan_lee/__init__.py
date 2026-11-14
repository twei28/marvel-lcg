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


def TraitsAPreter(player: 'Player') -> Dict[str, List[str]]:
    """Traits des identites empruntees, par type de face (« Hero » / « AlterEgo »).

    Une carte signature teste souvent un TRAIT de l'identite et non son nom
    (« only_if_your_identity_has_trait INVISIBLE », une amelioration reservee a un
    allie DORA MILAJE, « YouAreInHeroFrom TINY »). La carte de Stan Lee dit qu'il a
    les boites de texte de ces heros : leurs traits, imprimes sur la carte, en font
    partie. Constat de la batterie du 21/10/2026 : Invisible Woman, Okoye et Wasp Sting
    etaient injouables pour lui faute de ces traits.
    """
    from cards.database import CardsDB

    traits: Dict[str, List[str]] = {"Hero": [], "AlterEgo": []}
    for set_name in SetsEmpruntes(player):
        for card_id in CardsDB.sets_cards.get(set_name, []):
            paper = CardsDB.papers.get(card_id)
            if paper is None or paper.type not in traits:
                continue
            if NomPropre(paper.name) == "Stan Lee":
                continue
            for trait in paper.traits:
                if trait not in traits[paper.type]:
                    traits[paper.type].append(trait)
    return traits


# Aptitudes d'identite PRETEES telles quelles : card_id de l'identite d'origine -> son type de face.
#
# ⚠ LISTE VOLONTAIREMENT COURTE, UN HEROS A LA FOIS. Prêter « toutes » les aptitudes d'identite
# est faux : la plupart piochent dans des cartes mises de cote (Phoenix Force, deck meteo,
# Invocation...) que Stan Lee n'a pas, et deux heros pretes qui partagent un deck additionnel
# ou un nom de compteur se melangeraient. Ne vont ici que les aptitudes qui ne manipulent que
# des jetons sur l'identite elle-meme.
#   War Machine : « Locked and Loaded » pose 5 jetons `ammo` en passant en forme heros ;
#   James Rhodes les retire en repassant alter-ego. Sans eux, Repulsor Beam, Scorched Earth
#   et Full Auto (cout en jetons ammo) sont impayables pour Stan Lee.
APTITUDES_PRETEES = {
    "23001a": "Hero",
    "23001b": "AlterEgo",
}


def PreterAptitudes(player: 'Player') -> None:
    """Enregistre, sur la face de Stan Lee du meme type, les aptitudes de `APTITUDES_PRETEES`
    des heros empruntes. Une seule fois par face (idempotent, comme `AppliquerMarvelous`)."""
    from cards.database import CardsDB

    empruntes = SetsEmpruntes(player)
    for card_id, type_de_face in APTITUDES_PRETEES.items():
        paper = CardsDB.papers.get(card_id)
        if paper is None or paper.set_name not in empruntes:
            continue
        abilities = CardsDB.FindAbilities(paper.card_id, paper.pack, paper.set_name)
        for face in player.GetAllIdentityFace():
            if face.paper.type != type_de_face:
                continue
            deja = face.__dict__.setdefault("_aptitudes_pretees", set())
            if card_id in deja:
                continue
            deja.add(card_id)
            face.ability.Add(*abilities)
            for ability in abilities:
                face.effect.Registers(ability)


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

    traits = TraitsAPreter(player)
    for face in player.GetAllIdentityFace():
        for nom in noms:
            if nom in face.consider_as.names:
                continue
            face.SetConsiderAs(face, 1, name=nom)
        for trait in traits.get(face.paper.type, []):
            if trait in face.consider_as.traits:
                continue
            face.SetConsiderAs(face, 1, trait=trait)

    PreterAptitudes(player)


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
