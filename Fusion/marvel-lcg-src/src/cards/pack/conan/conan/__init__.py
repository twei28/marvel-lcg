from cards.pack import *
# Mot-cle officiel « Discount X (TRAIT) » : meme fabrique que Fear No Evil
# (60023 Know Your Enemy), reutilisee telle quelle.
from cards.pack.fne import DiscountAbility
from game.card.face.attribute.can_place_counter import CanPlaceCounter

# ---------------------------------------------------------------------------
# Pack custom « Conan » (RyCoRan, meme gabarit que Red Sonja), 25/09/2026.
# Journal : .planning/todos/2026-09-25-portage-conan.md
#
# L'identite est UNE carte a CINQ faces (modele Moon Knight mk001a-e,
# changement de forme d'Ant-Man 12001a/b/c) :
#   cn001a  Conan the Thief      (heros)
#   cn001b  Conan                (alter-ego de depart, CIMMERIA. THIEF.)
#   cn001c  Conan the Barbarian  (heros)
#   cn001d  King Conan           (heros, mis de cote au Setup)
#   cn001e  Conan                (alter-ego roi, mis de cote au Setup)
# Une seule carte = un seul cadran de PV, des statuts et des rencontres
# partages entre toutes les formes, comme l'exige l'insert.
#
# « Set King Conan aside » : les faces cn001d/e portent le drapeau moteur
# `hors_pile_identite` (player_setup.py / player_get.py, AJOUT du
# 25/09/2026). Elles ne sont alors proposees ni au changement volontaire ni
# aux effets « change to hero/alter-ego form ». Au couronnement (8 compteurs
# Crom sur The Cimmerian), le drapeau passe sur cn001a/b/c : « Remove your
# other identities from the game ».
# ---------------------------------------------------------------------------

NOM_CIMMERIAN = "The Cimmerian"

ID_VOLEUR = "cn001a"
ID_ALTER = "cn001b"
ID_BARBARE = "cn001c"
ID_ROI = "cn001d"
ID_ALTER_ROI = "cn001e"
FACES_DEPART = (ID_VOLEUR, ID_ALTER, ID_BARBARE)
FACES_ROI = (ID_ROI, ID_ALTER_ROI)

ID_CIMMERIAN_TITRE = "cn012a"
ID_CIMMERIAN_ROI = "cn012b"
ID_CITADELLE = "cn009"


def JoueurDe(effect: 'Effect') -> 'Player|None':
    joueur = effect.GetInitiator()
    return joueur if isinstance(joueur, Player) else None


def TrouverCimmerian(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    """The Cimmerian en jeu sous le controle de ce joueur (l'une ou l'autre face)."""
    for face in Worlds.FindCardsOnField(effect, card_type=Upgrade):
        if face.paper.card_id in (ID_CIMMERIAN_TITRE, ID_CIMMERIAN_ROI) and \
                face.GetControlBy() == joueur:
            return face
    return None


def CromSur(joueur: 'Player', effect: 'Effect') -> int:
    cim = TrouverCimmerian(joueur, effect)
    return cim.CastTo(CanPlaceCounter).GetCounters('crom') if cim else 0


def PoserCrom(joueur: 'Player|None', nombre: int, effect: 'Effect') -> None:
    """« Place N Crom counters on The Cimmerian ». Sans Cimmerian en jeu : rien."""
    if joueur is None or nombre <= 0:
        return
    cim = TrouverCimmerian(joueur, effect)
    if cim is not None:
        Faces.PlaceCountersOn([cim], nombre, 'crom', effect)


def EstKingConan(joueur: 'Player|None') -> bool:
    """« if you are King Conan » : la face heros cn001d est l'identite en jeu."""
    if joueur is None:
        return False
    identite = joueur.GetIdentity()
    return identite is not None and identite.paper.card_id == ID_ROI


def FacesIdentite(joueur: 'Player') -> List['CardFace']:
    identite = joueur.GetIdentity()
    return [f for f in [identite] + list(identite.card.back_faces)
            if f.paper.card_id.startswith("cn001")]


def FaceIdentite(joueur: 'Player', card_id: str) -> 'CardFace|None':
    for f in FacesIdentite(joueur):
        if f.paper.card_id == card_id:
            return f
    return None


def MarquerHorsPile(joueur: 'Player', hors_pile: Sequence[str]) -> None:
    """Pose le drapeau moteur `hors_pile_identite` sur exactement ces faces."""
    for f in FacesIdentite(joueur):
        setattr(f, 'hors_pile_identite', f.paper.card_id in hors_pile)


def Couronner(joueur: 'Player', effect: 'Effect') -> None:
    """The Cimmerian (cn012a), a 8 compteurs Crom : « ready your identity and
    swap him with King Conan. Remove your other identities from the game.
    Flip this card. »

    Arbitrage utilisateur du 25/09/2026 : l'echange GARDE LE COTE (heros ->
    King Conan heros, alter-ego -> Conan roi alter-ego) et n'est PAS un
    changement de forme. D'ou `FlipTo` direct, sans les messages
    WhenUnitWouldChangeForm / AfterUnitChangeForm que `ChangeToFace` envoie :
    ni Battle-Forged (cn001e) ni Frozen Ambush (cn014) ne se declenchent.
    """
    identite = joueur.GetIdentity()
    Faces.ReadyAll([identite], effect)
    vers = ID_ROI if Hero.IsType(identite) else ID_ALTER_ROI
    cible = FaceIdentite(joueur, vers)
    MarquerHorsPile(joueur, FACES_DEPART)
    if cible is not None and joueur.GetIdentity() != cible:
        joueur.GetIdentity().FlipTo(effect, card_face=cible)
    cim = TrouverCimmerian(joueur, effect)
    if cim is not None and cim.paper.card_id == ID_CIMMERIAN_TITRE:
        verso = [f for f in cim.card.back_faces if f.paper.card_id == ID_CIMMERIAN_ROI]
        if verso:
            cim.FlipTo(effect, card_face=verso[0])


# ---------------------------------------------------------------------------
# Rogue's Intuition (cn001a) et Born of Battle (cn001c) : seuil CUMULE par
# cible sur la phase (arbitrage utilisateur du 25/09/2026, lecture confirmee
# par l'insert : « it is 1 enemy or 1 scheme »). Comptent Conan, ses
# evenements, ses ameliorations et ressources ; PAS Bealit (alliee) : les
# regles (RRG, Ally) disent que ce que fait un allie n'est pas fait par
# l'identite du joueur.
#
# Le suivi vit sur l'objet `Card` de l'identite (jamais un dict global : un
# processus peut heberger plusieurs parties). Une meme condition peut etre
# evaluee plusieurs fois pour un meme message : le resultat est donc memorise
# PAR MESSAGE (comparaison d'identite `is`), et le cumul n'est augmente
# qu'une fois.
# ---------------------------------------------------------------------------

def _SuiviPhase(joueur: 'Player', effect: 'Effect') -> Dict[str, Any]:
    carte = joueur.GetIdentity().card
    phase = (effect.world.round_id, effect.world.phase.IsVillainPhase())
    suivi = getattr(carte, 'conan_suivi_crom', None)
    if suivi is None or suivi['phase'] != phase:
        suivi = {'phase': phase, 'cumul': [], 'messages': []}
        setattr(carte, 'conan_suivi_crom', suivi)
    return suivi


def SourceDuJoueur(source: 'CardFace|None', joueur: 'Player') -> bool:
    """La source est-elle Conan ou une carte qu'il controle, hors allie ?"""
    if source is None or Ally.IsType(source):
        return False
    try:
        return source.GetControlByOrOwner() == joueur
    except Exception:
        return False


def FranchitLeSeuil(joueur: 'Player', effect: 'Effect', message: Any,
                    cible: 'CardFace', montant: int, seuil: int, genre: str) -> bool:
    """Ajoute `montant` au cumul de `cible` pour la phase et rend True si CE
    message fait passer la cible de < seuil a >= seuil (une seule fois par
    cible et par phase)."""
    suivi = _SuiviPhase(joueur, effect)
    for (m, resultat) in suivi['messages']:
        if m is message:
            return resultat
    resultat = False
    if montant > 0:
        entree = None
        for e in suivi['cumul']:
            if e[0] == genre and e[1] is cible:
                entree = e
                break
        if entree is None:
            entree = [genre, cible, 0]
            suivi['cumul'].append(entree)
        avant = entree[2]
        entree[2] = avant + montant
        resultat = avant < seuil <= entree[2]
    suivi['messages'].append((message, resultat))
    return resultat


def ChoisirDegatsOuMenace(joueur: 'Player', this: 'CardFace', effect: 'Effect',
                          degats: int, menace: int) -> None:
    """« deal N damage to an enemy or remove M threat from a scheme »."""
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            f"Deal {degats} damage to an enemy",
            lambda cibles: this.DealDamage(list(cibles), degats, effect),
        ).SetTarget(Enemy, range=(1, 1)),
        AbilityFactory.ForChoiceAbility(
            f"Remove {menace} threat from a scheme",
            lambda cibles: this.RemoveThreatFromSchemes(list(cibles), menace, effect),
        ).SetTarget(Scheme2, range=(1, 1)),
    )


def DonnerStatutAUnEnnemi(joueur: 'Player', effect: 'Effect', statut: str, libelle: str) -> None:
    """« confuse an enemy » / « stun an enemy » : le joueur choisit l'ennemi."""
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            libelle,
            lambda cibles: Faces.GiveStatus(list(cibles), statut, effect),  # type: ignore
        ).SetTarget(Enemy, range=(1, 1)),
    )


# ---------------------------------------------------------------------------
# The Scarlet Citadel (cn009) : « While The Scarlet Citadel is in the victory
# display, if you have the THIEF trait, you get +1 THW and ignore the patrol
# keyword ; BARBARIAN : +1 ATK and ignore the guard keyword ; KING : all of
# the above. » Recette §3bis : une carte en vitrine n'enregistre AUCUNE
# capacite, le bonus vit donc sur les faces HEROS de l'identite, chacune
# selon SON trait (Thief : THW + patrouille, Barbarian : ATK + garde, King :
# tout). Les alter-ego n'ont ni THW ni ATK a augmenter et ne contrent ni
# n'attaquent : rien a y poser.
# ---------------------------------------------------------------------------

def CitadelleEnVitrine(effect: 'Effect') -> bool:
    return any(f.paper.card_id == ID_CITADELLE for f in Worlds.VictoryDisplay(effect).GetAll())


def CapacitesCitadelle(thw: bool, atk: bool) -> List['Ability']:
    capacites: List['Ability'] = []
    vitrine = OnEvent.Victory(CardFinder(name="The Scarlet Citadel"))
    if thw:
        capacites.append(AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if CitadelleEnVitrine(effect) else 0,
            thwart=1, change_on_event=vitrine,
        ).SetName("The Scarlet Citadel"))
        capacites.append(AbilityFactory.UnitIgnoreKeywordIcons(
            "You", patrol=True,
            conditions=[lambda effect, message: CitadelleEnVitrine(effect)],
        ).SetName("The Scarlet Citadel"))
    if atk:
        capacites.append(AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if CitadelleEnVitrine(effect) else 0,
            attack=1, change_on_event=vitrine,
        ).SetName("The Scarlet Citadel"))
        capacites.append(AbilityFactory.UnitIgnoreKeywordIcons(
            "You", guard=True,
            conditions=[lambda effect, message: CitadelleEnVitrine(effect)],
        ).SetName("The Scarlet Citadel"))
    return capacites
