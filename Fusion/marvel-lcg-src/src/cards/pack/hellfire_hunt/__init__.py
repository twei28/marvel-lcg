from cards.pack import *

# ===========================================================================
# Pack HELLFIRE HUNT (campagne de Dipsome), FONDATIONS : les cartes de campagne (16 allies RECRUITED hf013-hf028, 12 manigances annexes
# POTENTIAL ALLY hf029-hf040, 7 manigances de campagne hf041-hf047, l'environnement Xavier's Institute hf048) et les cartes d'aspect
# de Marvel Girl absentes du jeu (hf001-hf009, reskins hf010-hf012). Prefixe `hf` (tools/prefixes_fanmade.json) PARTAGE avec le pack des
# scenarios `hellfire_hunt_white_queen` (hf100+ : autre agent). Pack PLAT : un module par carte, `hfNNN.py`.
#
# ⚠ Les modules font `from . import *` : tout helper que les cartes appellent vit ICI (un NameError dans un helper est AVALE par le
# moteur et la capacite « ne part jamais » : lecon hk005).
# ===========================================================================


def JoueurDe(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (ou son initiateur)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def IdentiteDe(effect: 'Effect') -> 'CardFace|None':
    joueur = JoueurDe(effect)
    return joueur.GetIdentity() if joueur is not None else None


def RecruterDepuisLeMisDeCote(effect: 'Effect', joueur: 'Player', nom: str) -> 'CardFace|None':
    """« The player who defeated this scheme searches <nom> from the set-aside area, put it into play under the player's control. »
    Cherche l'allie nomme dans la zone mise de cote (mise en place de campagne) et le met en jeu sous le controle du joueur.
    Rend la carte, ou None si elle n'est pas (ou plus) de cote."""
    faces = Worlds.GetSetAsideAreaCards(effect, CardFinder(name=nom, card_type=Ally))
    if not faces:
        return None
    face = faces[0]
    face.PutIntoPlay(joueur, effect, under_control=True)
    return face


# ----------------------------------------------------------------------------------------------------------------------------
# E2 : le deck « Recruited Mutants » (deck de TABLE partage, avec sa propre defausse). Il n'existe pas dans le moteur (decks annexes
# par joueur seulement : `player.additional_deck`). On le cree a la demande, a un seul exemplaire par partie, comme deck de type
# AdditionalDeck / AdditionalDiscardPile rattache au SCENARIO (pas a une carte : un environnement n'a pas de controleur, et le deck
# doit survivre au depart de Xavier's Institute, scenario 5 : il est alors pose a cote de Rally the Survivors).
# ----------------------------------------------------------------------------------------------------------------------------
class DeckDeTable(Deck2):
    """Deck commun a la table : son PROPRIETAIRE est le joueur DONT C'EST LE TOUR. Le gestionnaire d'evenements ne laisse jouer une carte
    d'une pile hors-jeu que si `area.GetOwner()` est le joueur qui demande (manager.py:`check_initiator`) : avec le scenario pour proprietaire,
    Blink n'etait JAMAIS offerte depuis la defausse Recruited. (Niveau MODULE : `verifier_api_cartes` ne voit pas les classes locales.)"""
    def GetOwner(self):
        return self.bind_owner.world.GetCurrentPlayer()


def RecruitedMutants(effect: 'Effect') -> 'Tuple[Deck, Deck]':
    """(deck, defausse) du Recruited Mutants deck de cette partie."""
    from game.deck.deck import Deck2
    from game.deck.deck_type import DeckType
    from game.card.face.card_face import CardFace

    monde = effect.world
    etat = getattr(monde, "hf_recruited", None)
    if etat is None:
        deck = DeckDeTable(monde.scenario, DeckType.AdditionalDeck, CardFace)
        defausse = DeckDeTable(monde.scenario, DeckType.AdditionalDiscardPile, CardFace)
        deck.BindDiscardPile(defausse, lambda deck, effect: None)
        monde.additional_decks.append(deck)
        monde.additional_discard_piles.append(defausse)
        etat = (deck, defausse)
        monde.hf_recruited = etat
    return etat


def AjouterAuxRecrutes(effect: 'Effect', faces: 'Sequence[CardFace]') -> None:
    """Met ces cartes dans le Recruited Mutants deck et le melange (mise en place de campagne : les allies gagnes)."""
    deck, defausse = RecruitedMutants(effect)
    Faces.MoveAllTo(list(faces), deck, effect)
    for face in faces:
        face.card.bind_discard_pile = defausse
    deck.Shuffle(effect)


def PiocherDesRecrutes(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« draw 1 card from the Recruited Mutants deck » : la carte du dessus va dans la main du joueur."""
    deck, defausse = RecruitedMutants(effect)
    if deck.GetSize() == 0 and defausse.GetSize() > 0:
        Faces.MoveAllTo(list(defausse.Get(True)), deck, effect)   # le deck se vide : il se remelange avec sa defausse
        deck.Shuffle(effect)
    face = deck.GetTop()
    if face is None:
        return None
    joueur.GainCard(face, effect)
    return face


def AbilitePotentialAlly(nom: str) -> 'Ability':
    """« When Defeated: The player who defeat this scheme searches <nom> from the set-aside area, put it into play under the player's control. »
    Commun aux 12 manigances annexes POTENTIAL ALLY (hf029-hf040) et a Emma Frost's Redemption, Cryptic Threatening Message, Tactical Help,
    Enemy of Enemy. Modele : 04141 Prison Camps (`WhenSchemeBeDefeated(..., has_defeating_player=True)` + `message.GetDefeatingPlayer()`)."""
    def recruter(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        # Une manigance defaite PAR UN EFFET (Cerebro Insights) n'a pas de joueur vainqueur : le joueur courant en tient lieu.
        joueur = message.defeating_player or effect.world.GetCurrentPlayer()      # `GetDefeatingPlayer()` leve une AssertionError sans joueur vainqueur
        RecruterDepuisLeMisDeCote(effect, joueur, nom)

    return AbilityFactory.WhenSchemeBeDefeated(
        AbilityType.WhenDefeated,
        "This",
        recruter,
        # PAS `has_defeating_player=True` : une manigance defaite PAR UN EFFET (Cerebro Insights) n'a pas de joueur vainqueur et l'aptitude ne partait pas.
    )


def PersonnageEnJeu(effect: 'Effect', noms: 'Sequence[str]') -> bool:
    """Vrai si un personnage AMI en jeu (identite ou allie) porte l'un de ces noms (titre OU sous-titre : « Captain Britain / Betsy Braddock »).
    Sert aux Team-Up que `desc.TeamUp` ne sait pas porter (soutien, alias d'un meme personnage)."""
    for face in Worlds.GetOnFieldFriendlyCharacters(effect):
        titre = face.paper.name.lstrip('* ').strip()
        sous_titre = (face.paper.subtitle or '').strip()
        if titre in noms or sous_titre in noms:
            return True
    return False


def PermissionDeJouerLesRecrutes() -> 'List[Ability]':
    """hf014 Blink : « Any of the players may play Blink from Recruited Mutant discard pile during their own turn (paying its resource cost) ».
    ⚠ Les capacites d'une carte qui dort dans une DEFAUSSE ne sont pas actives : la permission ne peut pas vivre sur Blink. On la porte donc par les
    cartes de campagne qui TIENNENT le deck Recruited Mutants a cote d'elles : Xavier's Institute (hf048, scenarios 1 a 4) et Rally the Survivors
    (hf045, scenario 5). Modele : dz014 / 53021 (`YouMayPlayCardLikeInHand`, play.py:436)."""
    def dans_la_defausse_des_recrutes(effect: 'Effect', message: 'Message.CheckIfFaceIsLikeInHand') -> bool:
        _, defausse = RecruitedMutants(effect)
        return message.which_face.card.area is defausse

    # « during their own turn » : un allie ne se joue que pendant un tour de joueur (action) ; `during="YourTurn"` exige `which_card == "This"`
    # (play.py:492) et le message n'indique pas le joueur : pas de condition de tour ici.
    return AbilityFactory.YouMayPlayCardLikeInHand(
        AbilityType.NonKeyword,
        CardFinder(name="Blink"),
        from_where="YourDiscardPile",
        conditions=[dans_la_defausse_des_recrutes],
    )
