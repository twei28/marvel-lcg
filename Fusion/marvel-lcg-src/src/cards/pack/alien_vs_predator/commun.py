from cards.pack import *

# Helpers partages des QUATRE sets d'Alien vs. Predator (RyCoRan, prefixe `ap`). Chaque `__init__.py` de set fait
# `from cards.pack.alien_vs_predator.commun import *` : c'est le seul moyen pour les modules de carte (`from . import *`) de les
# voir (lecon hk005, voir le `__init__.py` du pack).

REINE = "Alien Queen"
WARLORD = "Predator Warlord"
HIVE = "Expanding Hive"
SKULLS = "Skulls for the Taking"
ULTIMATE_HUNT = "The Ultimate Hunt"
DEFAITE = "DEFEATED"
# « Alien Queen's Scheme. » / « Predator Warlord's Scheme. » (imprime en tete des deux manigances permanentes).
MANIGANCE_DE = {REINE: HIVE, WARLORD: SKULLS}
TRAIT_DE = {REINE: "XENOMORPH", WARLORD: "YAUTJA"}
IDS_SCOUTS = ("ap101", "ap102", "ap103", "ap104")


################################################################################
# Les deux mechants et le compteur actif
def NomDuMechant(face: 'CardFace|None') -> str:
    """« Alien Queen » ou « Predator Warlord » (le nom, jamais le card_id : faces A/B standard et expert)."""
    if face is None:
        return ""
    for nom in MANIGANCE_DE:
        if face.IsName(nom):
            return nom
    return ""


def Mechants(effect: 'Effect') -> List['Villain']:
    """Les mechants VIVANTS en jeu (la face « Defeated », de passage, n'en est plus un), de gauche a droite."""
    return [v for v in Villains.All(effect) if NomDuMechant(v) and not v.HasTrait(DEFAITE)]


def MechantNomme(effect: 'Effect', nom: str) -> 'Villain|None':
    for v in Mechants(effect):
        if v.IsName(nom):
            return v
    return None


def MechantActif(effect: 'Effect') -> 'Villain|None':
    """« The active villain » : celui qui porte le compteur actif ; a defaut (compteur disparu avec un mechant vaincu), le
    seul ou le premier mechant vivant."""
    actif = Villains.Active(effect)
    if actif is not None and NomDuMechant(actif) and not actif.HasTrait(DEFAITE):
        return actif
    vivants = Mechants(effect)
    return vivants[0] if vivants else None


def EstLeMechantActif(effect: 'Effect', nom: str) -> bool:
    actif = MechantActif(effect)
    return actif is not None and actif.IsName(nom)


def GarderLeCompteur(effect: 'Effect') -> None:
    """« Do not move the active villain counter » (Advance Again, Assault, Boost d'Alien Assault) : le prochain deplacement
    du compteur est annule (consomme par `PasserLeCompteur`)."""
    effect.world._ap_garder_compteur = True


def OublierLaGarde(effect: 'Effect') -> None:
    effect.world._ap_garder_compteur = False


def PasserLeCompteur(effect: 'Effect') -> bool:
    """« Move the active counter to the next villain » : vers l'AUTRE mechant vivant. Sans effet s'il n'en reste qu'un, ou si
    une carte a dit « do not move » pour cette activation (la garde est alors consommee). Rend True si le compteur a bouge."""
    if getattr(effect.world, '_ap_garder_compteur', False):
        OublierLaGarde(effect)
        return False
    actif = MechantActif(effect)
    autres = [v for v in Mechants(effect) if v is not actif]
    if not autres:
        return False
    Villains.SetActive(autres[0], effect)
    return True


def ManiganceDe(effect: 'Effect', nom_mechant: str) -> 'EncounterSideScheme|None':
    """La manigance annexe permanente du mechant (« his / her side scheme »), si elle est en jeu."""
    nom = MANIGANCE_DE.get(nom_mechant)
    if not nom:
        return None
    trouvees = Worlds.FindCardsOnField(effect, name=nom, card_type=EncounterSideScheme)
    return trouvees[0] if trouvees else None


def ManigancesPermanentes(effect: 'Effect') -> List['EncounterSideScheme']:
    return [m for m in (ManiganceDe(effect, REINE), ManiganceDe(effect, WARLORD)) if m is not None]


def NombreDeJoueurs(effect: 'Effect') -> int:
    return max(1, len(Worlds.GetPlayers(effect)))


def LeComplot(effect: 'Effect') -> 'MainScheme|None':
    complots = Worlds.GetMainSchemes(effect)
    return complots[0] if complots else None


################################################################################
# Le deck Xenomorph (16 Alien Scout glisses sous Alien Queen, face cachee)
def DeckXenomorph(effect: 'Effect') -> List['CardFace']:
    """Les Alien Scout du deck Xenomorph (« placed next to the Alien Queen ») : glisses SOUS la Reine a la mise en place."""
    reine = MechantNomme(effect, REINE)
    if reine is None:
        return []
    return [f for f in reine.GetPlacedCardArea().GetAll() if f.paper.card_id in IDS_SCOUTS]


def MelangerUnXenomorph(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    """« Shuffle a Xenomorph card into your deck » : une carte AU HASARD du deck Xenomorph (deck melange face cachee) dans le
    deck du joueur, puis melange. Insert : « Once this deck is empty ... no other cards are shuffled » (rend None)."""
    deck = DeckXenomorph(effect)
    if not deck or joueur is None:
        return None
    carte = Rand.RandomChoice(deck, effect)
    Faces.ShuffleAllTo([carte], joueur.player_deck, effect)
    return carte


################################################################################
# Joueurs
def JoueurDuMessage(message: 'Message2', effect: 'Effect') -> 'Player':
    """« you » d'une carte de rencontre : le joueur du message, sinon le joueur courant, sinon le premier joueur."""
    try:
        joueur = message.GetToPlayer()
    except Exception:
        joueur = None
    if Player.IsType(joueur):
        return joueur
    courant = effect.world.current_player
    if Player.IsType(courant):
        return courant
    return Worlds.GetFirstPlayer(effect)


def JoueurQuiVainc(message: 'Message.WhenUnitBeDefeated', effect: 'Effect', face: 'CardFace|None'=None) -> 'Player':
    """« you » d'un « When Defeated » de sbire : le joueur qui l'a vaincu, sinon le joueur engage avec lui, sinon le premier."""
    for nom in ("defeating_player", "by_player"):
        j = getattr(message, nom, None)
        if Player.IsType(j):
            return j
    ini = getattr(getattr(message, "by_effect", None), "initiator", None)
    if Player.IsType(ini):
        return ini
    if face is not None and Minion.IsType(face):
        try:
            engage = face.CastTo(Minion).GetEngagedPlayer()
        except Exception:
            engage = None
        if Player.IsType(engage):
            return engage
    return Worlds.GetFirstPlayer(effect)


################################################################################
# Petites briques
def BoostReveleCetteCarte() -> 'Ability':
    """« [star] Boost: Reveal this card. » (modele tk : `RevealThisCard`)."""
    return AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard)


def SbiresParTrait(effect: 'Effect', trait: str) -> List['Minion']:
    return [m for m in Worlds.GetOnFieldMinions(effect) if m.HasTrait(trait)]


def EnnemisParTrait(effect: 'Effect', trait: str) -> List['CardFace']:
    return [e for e in Worlds.GetOnFieldEnemies(effect) if e.HasTrait(trait)]


def ChercherEtReveler(effect: 'Effect', joueur: 'Player', trait: str) -> 'CardFace|None':
    """« Search the encounter deck and discard pile for a [[TRAIT]] minion and reveal it »."""
    sbire = Search.EncounterCard(effect, joueur, include_discard_pile=True, trait=trait, card_type=Minion)
    if sbire is None:
        return None
    sbire.Reveal(joueur, effect)
    return sbire


def DefausserJusquAReveler(effect: 'Effect', joueur: 'Player', **finder) -> 'CardFace|None':
    """« Discard cards from the top of the encounter deck until a X is discarded. Reveal it. »"""
    carte = Worlds.DiscardEncounterCardsUntil(effect, **finder)
    if carte is not None:
        carte.Reveal(joueur, effect)
    return carte


def IconesDeBoost(face: 'CardFace|None') -> int:
    """« each icon ([star] and [boost]) in that card's boost area » (modele pd008)."""
    if face is None:
        return 0
    return FacesCounter.CountTotalBoostIcons([face]) + FacesCounter.CountTotalBoostStar([face])


def DonnerCommeBoost(face: 'CardFace', effect: 'Effect') -> bool:
    """« Give this card to the active villain as a facedown boost card » (modele 60075)."""
    actif = MechantActif(effect)
    if actif is None:
        return False
    actif.GiveBoostCard(face, effect)
    return True


def EncoreLibre(face: 'CardFace') -> bool:
    """La carte n'a pas ete donnee comme carte boost entre-temps (Expanding Hive passe AVANT le « When Defeated » du sbire : la
    carte reste alors en boost, arbitrage du 25/10/2026)."""
    return not face.card.area.flags.is_attach_boost_area


def AttacherAuWarlordSinonYautja() -> 'Ability':
    """« Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge. »
    (Yautja Wrist Blades, Cloaking Device)."""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(
        CardFinder(name=WARLORD, card_type=Villain),
        if_cannot_attach_to=Select.From(CardFinder(card_type=Minion, trait="YAUTJA")),
        if_cannot_gain_surge=True)
