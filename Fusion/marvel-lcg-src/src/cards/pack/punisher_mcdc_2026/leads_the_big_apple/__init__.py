from ..commun import *

# Set Leads - The Big Apple (pack MC×DC 2026) : les 9 PISTES (obligations LEAD, une par lieu), melangees dans le paquet LEADS commun a la
# table (`Worlds.ScenarioDeck(effect, "LeadsDeck")`, modele PlanetDeck de skrull_empire). Chaque joueur en revele une a la mise en place
# (Gang War 1A) ; une obligation revelee va dans l'aire de jeu du joueur qui la revele (`Obligation.OnPlayerRevealCard`).
#
# Forme commune : « Response : While in <lieu>, after <evenement>, place 1 <compteur> counter here. Then, if there are N or more counters
# here, add this card to the victory display, reveal the top LEAD card, and draw 1 card. »
#   - « While in <lieu> » : lu AU DECLENCHEMENT (`EnLieu`), pas en continu : les compteurs deja poses restent si on part ;
#   - « you » = le joueur dans l'aire duquel la piste se trouve (`Joueur`) ;
#   - fin commune : `PisteTerminee` (victoire, nouvelle piste, 1 carte).

LIEUX = {"pu030": "Hell's Kitchen", "pu031": "Theater District", "pu032": "Upper East Side", "pu033": "West Village", "pu034": "Midtown",
         "pu035": "Lower East Side", "pu036": "Soho", "pu037": "Financial District", "pu038": "Chinatown"}


def Joueur(effect: 'Effect') -> 'Player|None':
    """Le joueur dans l'aire duquel se trouve la piste (zone des obligations) : `GetGaveToPlayer`, pas `GetControlByOrOwner` (qui rend le
    vilain pour une obligation)."""
    face = effect.this
    if not Obligation.IsType(face):
        return None
    try:
        return face.CastTo(Obligation).GetGaveToPlayer()
    except AssertionError:
        return None


def EnLieu(carte_lieu: str) -> 'Callable[[Effect, Message2], bool]':
    """Condition « While in <lieu> » : le joueur qui porte la piste occupe le lieu `carte_lieu` (card_id pu030..pu038)."""
    def condition(effect: 'Effect', message: 'Message2') -> bool:
        joueur = Joueur(effect)
        if joueur is None:
            return False
        lieu = Ville.Lieu(effect, joueur)
        return lieu is not None and lieu.paper.card_id == carte_lieu
    return condition


def ControlePar(face: 'CardFace', joueur: 'Player') -> bool:
    return face.GetControlByPlayer() is joueur


def PaquetPistes(effect: 'Effect') -> 'SetAsideDeck':
    return Worlds.ScenarioDeck(effect, "LeadsDeck")


def CreerPaquetPistes(effect: 'Effect', proprietaire: 'Villain') -> None:
    """« Create the 9-card LEADS deck » : les pistes mises de cote, melangees, face cachee (modele `CreerPaquetPlanete`)."""
    paquet = PaquetPistes(effect)
    paquet.Create(effect, proprietaire, type=DeckType.AdditionalDeck, has_discard_pile=False)
    faces = [f for f in Worlds.AsideDeck(effect).Get(True) if f.HasTrait("LEAD")]
    Faces.ShuffleAllTo(faces, paquet.deck, effect)


def RevelerPiste(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« Reveal the top LEAD card » : paquet vide ou absent, rien. La piste va dans l'aire du joueur qui la revele."""
    paquet = PaquetPistes(effect)
    if not paquet.initialize:
        return None
    face = paquet.GetTopCard()
    if face is None:
        return None
    face.Reveal(joueur, effect)
    return face


def PistesEnVictoire(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.VictoryDisplay(effect).Get(True) if f.HasTrait("LEAD")]


def PisteTerminee(effect: 'Effect', joueur: 'Player') -> None:
    """« Add this card to the victory display, reveal the top LEAD card, and draw 1 card. »"""
    Faces.AddToVictoryDisplay([effect.this], effect)
    RevelerPiste(effect, joueur)
    joueur.DrawUp(1, effect)


def CompteurPuisFin(effect: 'Effect', joueur: 'Player', compteur: str, seuil: int) -> None:
    """« place 1 <compteur> counter here. Then, if there are <seuil> or more counters here, [PisteTerminee]. »"""
    this = effect.this
    Faces.PlaceCountersOn([this], 1, compteur, effect)
    if this.GetCounters(compteur) >= seuil:
        PisteTerminee(effect, joueur)
