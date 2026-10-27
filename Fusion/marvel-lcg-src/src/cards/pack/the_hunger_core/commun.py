from cards.pack import *

# Helpers partages de TOUS les sets du scenario « The Hunger Core » (Marvel Zombies, fan-made, Penasquequeman,
# prefixe `hg`). Chaque `__init__.py` de set fait `from cards.pack.the_hunger_core.commun import *` (lecon hk005,
# modele `alien_vs_predator/commun.py`).
#
# Regles source : livret officiel du scenario (PDF, 9 pages, recupere depuis le fichier TTS), pages 3-6.

CORE = "The Hunger Core"
TRAIT_METAZOMBIE = "METAZOMBIE"

# Stade courant du Coeur -> card_id de son PROCHAIN stade (« Deeper Inside », page 5). I->II en Standard,
# II->III en Expert ; III n'a pas de suite (ne devrait jamais etre demande).
PROCHAIN_STADE_COEUR = {1: "hg002", 2: "hg003"}

NOMS_HORDE = (
    "Zombie Captain America", "Zombie Iron Man", "Zombie Hulk", "Zombie Spider-Man",
    "Zombie Captain Marvel", "Zombie Thor", "Zombie Black Widow", "Zombie Doctor Strange", "Zombie Magik",
)

CARD_ID_HORDE = {
    "Zombie Captain America": "hg007", "Zombie Iron Man": "hg008", "Zombie Hulk": "hg009",
    "Zombie Spider-Man": "hg010", "Zombie Captain Marvel": "hg011", "Zombie Thor": "hg012",
    "Zombie Black Widow": "hg013", "Zombie Doctor Strange": "hg014", "Zombie Magik": "hg015",
}

# « Set aside the zombie version of each chosen hero » (page 7) : nom du HEROS reel (celui choisi par le
# joueur, sans « Zombie ») -> card_id de sa version zombie, dans le Horde deck OU dans Fallen Heroes.
CARD_ID_HORDE_PAR_HEROS = {nom[len("Zombie "):]: cid for nom, cid in CARD_ID_HORDE.items()}

NOMS_FALLEN = (
    "Luke Cage", "Hawkeye", "Giant-Man", "Wasp", "Nova Prime", "Mister Fantastic",
    "Invisible Woman", "Thing", "Human Torch", "Rhino", "Colossus", "Falcon", "Quicksilver",
)
CARD_ID_FALLEN_PAR_HEROS = {
    "Luke Cage": "hg059", "Hawkeye": "hg060", "Giant-Man": "hg061", "Wasp": "hg062",
    "Nova Prime": "hg063", "Mister Fantastic": "hg064", "Invisible Woman": "hg065",
    "Thing": "hg066", "Human Torch": "hg067", "Rhino": "hg068", "Colossus": "hg069",
    "Falcon": "hg070", "Quicksilver": "hg071",
}

# Les 5 allies du Survivor deck PARTAGENT leur nom avec des heros jouables officiels (Wolverine, Blade) :
# page 7, « If someone plays one of those heroes (for example, Wolverine), remove that ally and its Trapped
# Survivor from the game. »
CARD_ID_SURVIVOR_SCHEME_PAR_HEROS = {
    "Franklin Richards": "hg051", "Chewie": "hg052", "Valeria Richards": "hg053",
    "Blade": "hg054", "Wolverine": "hg055",
}
CARD_ID_SURVIVOR_ALLY_PAR_HEROS = {
    "Franklin Richards": "hg072", "Chewie": "hg073", "Valeria Richards": "hg074",
    "Blade": "hg075", "Wolverine": "hg076",
}

# card_id (sans face) -> liste des card_id de son deck signature, DANS L'ORDRE imprime (peu importe, il est
# melange a la construction). Page 4 : « 3 cards; 5 for Zombie Iron Man and 6 for Zombie Captain Marvel ».
DECKS_SIGNATURE = {
    "Zombie Captain America": ["hg016", "hg017", "hg018"],
    "Zombie Iron Man": ["hg019", "hg020", "hg021", "hg022", "hg023"],
    "Zombie Hulk": ["hg024", "hg025", "hg026"],
    "Zombie Spider-Man": ["hg027", "hg028", "hg029"],
    "Zombie Captain Marvel": ["hg030", "hg031", "hg032", "hg033", "hg033", "hg033"],
    "Zombie Thor": ["hg034", "hg035", "hg036"],
    "Zombie Black Widow": ["hg037", "hg038", "hg039"],
    "Zombie Doctor Strange": ["hg040", "hg041", "hg042"],
    "Zombie Magik": ["hg043", "hg044", "hg045"],
}

MAX_METAZOMBIES_EN_JEU = 3


################################################################################
# Le Coeur et les Metazombies, tous des VILLAIN (page 3 : « A Metazombie is a villain for all purposes »)
def LeCoeur(effect: 'Effect') -> 'Villain|None':
    """« The Hunger Core », quel que soit son stade (I/II/III : meme nom, trois card_id distincts)."""
    for v in Villains.All(effect):
        if v.IsName(CORE):
            return v
    return None


def Metazombies(effect: 'Effect') -> List['Villain']:
    """Les Metazombies VIVANTS en jeu, dans l'ordre d'entree (gauche -> droite de la rangee, page 3)."""
    return [v for v in Villains.All(effect) if v.HasTrait(TRAIT_METAZOMBIE)]


def NbMetazombiesEnJeu(effect: 'Effect') -> int:
    return len(Metazombies(effect))


def ProchainStadeDuCoeur(effect: 'Effect', coeur: 'Villain') -> 'Villain|None':
    """« Remove the Core card from the game and put its next stage into play (II in Standard, III in
    Expert). » Genere une carte NEUVE (le stade suivant n'existe pas encore en jeu) ; `Villain.Advance` fait le
    reste (meme nom sur les trois stades -> `SetAsCard`, meme Card, `call_reveal=True`)."""
    from game.card.factory import CardFactory
    suivant_id = PROCHAIN_STADE_COEUR.get(coeur.printed_stage)
    if suivant_id is None:
        return None
    carte = CardFactory.GenerateCard(suivant_id, effect.world.aside_deck, effect.world)
    return carte.face.CastTo(Villain)


def LeMetazombieActif(effect: 'Effect') -> 'Villain|None':
    """« The active Metazombie token decides which villain activates. » A defaut (jeton tombe sur le Coeur ou
    disparu avec un Metazombie vaincu), le premier Metazombie vivant, sinon le Coeur."""
    actif = Villains.Active(effect)
    if actif is not None and (actif.HasTrait(TRAIT_METAZOMBIE) or actif.IsName(CORE)) and actif.IsInPlay():
        return actif
    vivants = Metazombies(effect)
    if vivants:
        return vivants[0]
    return LeCoeur(effect)


def PasserLeJeton(effect: 'Effect') -> None:
    """« At the end of each villain phase, the token moves to the next Metazombie in the row, to the right. From
    the last one it goes back to the first. If no Metazombie is left, the token moves to The Hunger Core. »"""
    vivants = Metazombies(effect)
    if not vivants:
        coeur = LeCoeur(effect)
        if coeur is not None:
            Villains.SetActive(coeur, effect)
        return
    actif = Villains.Active(effect)
    if actif in vivants:
        i = vivants.index(actif)
        suivant = vivants[(i + 1) % len(vivants)]
    else:
        suivant = vivants[0]
    Villains.SetActive(suivant, effect)


def JetonApresDefaite(effect: 'Effect', vaincu: 'Villain') -> None:
    """« If the active Metazombie is defeated, the token moves IMMEDIATELY to the next one in the row, which
    resolves any remaining activations. If no Metazombie is left, the token moves to The Hunger Core. » Distinct
    de `PasserLeJeton` (fin de ronde normale). Appele depuis `QuandMetazombieVaincu`, au moment du
    `WhenUnitBeDefeated` : le vaincu est ENCORE dans la rangee (meme timing que Sinister Six,
    `MoveTheActiveCounterToTheNextVillain`), d'ou le calcul « le suivant A DROITE du vaincu, en bouclant »,
    vaincu exclu. (Avant le 27/10/2026, on prenait `vivants[0]` : faux des que le vaincu n'etait pas le premier.)"""
    rangee = Metazombies(effect)
    if vaincu in rangee:
        i = rangee.index(vaincu)
        candidats = rangee[i + 1:] + rangee[:i]
    else:
        candidats = rangee
    if candidats:
        Villains.SetActive(candidats[0], effect)
        return
    coeur = LeCoeur(effect)
    if coeur is not None:
        Villains.SetActive(coeur, effect)


################################################################################
# Le Horde deck (page 3, 6 : 9 Metazombies facedown, JAMAIS melanges au deck de rencontre, distinct du deck des
# 13 Fallen Heroes qui, lui, EST melange dans le deck de rencontre). Modele `player.additional_deck` /
# `additional_discard_pile` (player.py:97-99), mais lie au SCENARIO et pas a un joueur : il n'appartient a
# personne, comme le veut « The game's Metazombies, facedown » du glossaire (page 6).
def _Scenario(effect: 'Effect') -> 'Scenario':
    return Worlds.CastWorld(effect).GetScenario()


def HordeDeck(effect: 'Effect') -> 'Deck2':
    scenario = _Scenario(effect)
    deck = getattr(scenario, 'hgc_horde_deck', None)
    if deck is None:
        deck = Deck2(scenario, DeckType.AdditionalDeck, Villain)
        discard = Deck2(scenario, DeckType.AdditionalDiscardPile, Villain)
        deck.BindDiscardPile(discard, lambda d, e: None)
        scenario.hgc_horde_deck = deck
        scenario.hgc_horde_discard = discard
    return deck


def HordeDiscard(effect: 'Effect') -> 'Deck2':
    HordeDeck(effect)  # cree les deux au besoin
    return _Scenario(effect).hgc_horde_discard


def ConstruireLeHordeDeck(effect: 'Effect', noms_heros_exclus: Sequence[str]) -> None:
    """Mise en place (hg004a) : « Shuffle the other Metazombies: this is the Horde deck. »
    `noms_heros_exclus` = noms REELS des heros choisis (« Captain America », pas « Zombie Captain America »)
    dont la version zombie est mise de cote."""
    from game.card.factory import CardFactory
    deck = HordeDeck(effect)
    for nom_reel, card_id in CARD_ID_HORDE_PAR_HEROS.items():
        if nom_reel in noms_heros_exclus:
            continue
        CardFactory.GenerateCard(card_id, deck, effect.world)
    deck.Shuffle(effect)


def MettreUnMetazombieEnJeu(effect: 'Effect', joueur: 'Player') -> 'Villain|None':
    """« Putting a Metazombie into play: take the top card of the Horde deck and place it at the right end of the
    row... If the Horde deck is empty, shuffle its discard pile to make a new one; if both are empty, nothing
    happens. Maximum 3: if something would put a fourth one into play, it does not enter. »"""
    if NbMetazombiesEnJeu(effect) >= MAX_METAZOMBIES_EN_JEU:
        return None
    deck = HordeDeck(effect)
    if deck.GetTop() is None:
        deck.ShuffleWithDiscardPile(False, effect)
    carte = deck.GetTop()
    if carte is None:
        return None
    # « If no Metazombie is left, the token moves to The Hunger Core. When a Metazombie enters play again, the
    # token moves to it. » (livret p. 4) + mise en place p. 7, etape 7 : « Place the active Metazombie token on
    # the first one in the row » (hg004a pose d'abord le jeton sur le Coeur, le 1er Metazombie le reprend ici).
    # Garde `coeur is not None` : hors scenario (cas montes sur Rhino), on ne touche jamais au jeton.
    coeur = LeCoeur(effect)
    actif_avant = Villains.Active(effect)
    carte.PutIntoPlay(joueur, effect)
    metazombie = carte.CastTo(Villain)
    if coeur is not None and (actif_avant is None or actif_avant is coeur) and metazombie.IsInPlay():
        Villains.SetActive(metazombie, effect)
    return metazombie


def QuandMetazombieVaincu(effect: 'Effect', metazombie: 'Villain') -> None:
    """« When a Metazombie is defeated: discard the cards attached to it, put it in the Horde discard pile and set
    its signature deck aside next to it. » (livret p. 3) + FAQ p. 8 : « A Metazombie with attachments is
    defeated. What happens to them? They go to the bottom of its signature deck. If that Metazombie comes back,
    it can use them again. » + p. 4 : jeton qui passe IMMEDIATEMENT au suivant si c'etait l'actif.

    Branche par `ReglesDuScenario` sur `WhenUnitBeDefeated` (AbilityType.Scenario), timing ou le vaincu est
    ENCORE en jeu (attachements compris). Le sortir ici vers la defausse du Horde deck fait que
    `Villain.OnBeDefeated` ne l'« avance » plus (`if self.IsInPlay()` faux) : sans ce crochet,
    `Scenario.AdvanceVillainStage` le RETIRAIT DE LA PARTIE (aucun stade suivant du meme nom), et il ne
    pouvait jamais revenir par le Horde deck."""
    from game.card.face.card_type import Attachment
    noms_signature = set(DECKS_SIGNATURE.get(metazombie.name, []))
    for attache in list(metazombie.GetInventoryDeck().GetAll()):
        if attache.paper.card_id in noms_signature:
            DefausserAuFondDuDeckSignature(effect, metazombie, attache)
        elif Attachment.IsType(attache):
            Faces.DiscardAll([attache], effect)
    if metazombie.IsActive():
        JetonApresDefaite(effect, metazombie)
    Faces.MoveAllTo([metazombie], HordeDiscard(effect), effect)


def ReglesDuScenario() -> List['Ability']:
    """Regles de scenario du livret qu'aucune carte n'imprime, posees UNE fois sur le Coeur (present du Setup a
    la victoire, ses trois stades appellent `CapacitesDuCoeur`, qui inclut cette liste). Type
    `AbilityType.Scenario`, modele Sinister Six (`sm/sinister_six/27100a.py`, compteur actif deplace sur
    `WhenUnitBeDefeated`).
    - fin de phase du mechant : le jeton tourne (`PasserLeJeton`) ;
    - Metazombie vaincu : `QuandMetazombieVaincu` (attachements, jeton, defausse du Horde deck) ;
    - « Infection. When an attack from a Zombie or Metazombie enemy deals damage to your hero, place 1
      Infection counter. » (livret p. 5) : `AfterUnitAttackAndDamageUnit(..., Hero, ...)` avec
      `target_took_damage=True` (« If an ally defends, or if your DEF or a tough status card prevents all the
      damage, there is no Infection ») ; 1 compteur par attaque, quels que soient les degats."""
    from game.card.face.base import Enemy

    # ⚠ Une capacite `AbilityType.Scenario` reste active HORS JEU : en standard, hg002 (stade II, encore dans le deck
    # des stades) declenchait chaque regle une 2e fois (jeton avance de DEUX crans, 2 Infections par morsure ; mesure
    # en autoplay le 27/10/2026, 3 fois en expert avec hg003). Seul le stade EN JEU applique les regles.
    def coeur_en_jeu(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        return effect.this.IsInPlay()

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        Unused(message)
        PasserLeJeton(effect)

    def metazombie_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        metazombie = message.trigger.CastTo(Villain)
        if metazombie.IsInPlay():
            QuandMetazombieVaincu(effect, metazombie)

    def est_un_zombie(face: 'CardFace') -> bool:
        return Enemy.IsType(face) and (face.HasTrait("ZOMBIE") or face.HasTrait(TRAIT_METAZOMBIE))

    def morsure(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        joueur = message.attacked.GetControlByOrOwner()
        if Player.IsType(joueur):
            PoserInfection(effect, joueur, 1)

    return [
        AbilityFactory.WhenVillainPhaseEnd(AbilityType.Scenario, fin_de_phase, conditions=[coeur_en_jeu]),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.Scenario, CardFinder(traits=[TRAIT_METAZOMBIE], card_type=Villain),
                                          metazombie_vaincu, conditions=[coeur_en_jeu]),
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.Scenario, CardFinder(check_face_fn=est_un_zombie),
                                                    Hero, morsure, conditions=[coeur_en_jeu]),
    ]


################################################################################
# Decks signature (page 4) : un petit deck PAR Metazombie, lie a SA carte (modele `Deck2(owner=Card, ...)`,
# jamais melange au deck de rencontre, la defausse d'une carte signature va au FOND de CE deck, pas a la
# defausse de rencontre).
def _DeckSignatureAttr(metazombie: 'Villain') -> str:
    return f"_hgc_sig_{id(metazombie.card)}"


def DeckSignatureDe(effect: 'Effect', metazombie: 'Villain') -> 'Deck2':
    """Cree (et melange, une seule fois) le deck signature du Metazombie a sa premiere consultation. « Shuffle its
    signature deck and place it facedown next to it »."""
    from game.card.factory import CardFactory
    attr = _DeckSignatureAttr(metazombie)
    deck = getattr(metazombie.card, attr, None)
    if deck is not None:
        return deck
    ids = DECKS_SIGNATURE.get(metazombie.name, [])
    deck = Deck2(metazombie.card, DeckType.AdditionalDeck, CardFace)
    setattr(metazombie.card, attr, deck)
    for cid in ids:
        CardFactory.GenerateCard(cid, deck, effect.world)
    deck.Shuffle(effect)
    return deck


def RevelerLeDessusDuDeckSignature(effect: 'Effect', metazombie: 'Villain', joueur: 'Player') -> 'CardFace|None':
    deck = DeckSignatureDe(effect, metazombie)
    carte = deck.GetTop()
    if carte is None:
        return None
    carte.Reveal(joueur, effect)
    return carte


def DefausserAuFondDuDeckSignature(effect: 'Effect', metazombie: 'Villain', carte: 'CardFace') -> None:
    """« A discarded signature card goes to the BOTTOM of its Metazombie's signature deck, not the encounter
    discard pile. »"""
    deck = DeckSignatureDe(effect, metazombie)
    carte.card.MoveToBottom(deck, effect)


def DefausserJusquaUneAmeliorationDuDeckSignature(effect: 'Effect', metazombie: 'Villain') -> 'CardFace|None':
    """« Discard cards from his signature deck until an attachment is discarded and attach it to him. Then
    shuffle the discarded cards into his signature deck. » Partage par hg008 Zombie Iron Man (a son entree en
    jeu) et hg023 Hunger Protocol (sa propre carte signature, When Revealed).

    Chaque carte non-amelioration suit la regle generale du deck signature (page 4, deja codee dans
    `DefausserAuFondDuDeckSignature`) : elle va au FOND du MEME deck, jamais a une defausse de rencontre. La
    boucle est bornee par la taille INITIALE du deck (`limite`) : chaque carte n'est examinee qu'une seule
    fois (deplacee du sommet vers le fond, jamais reinseree au-dessus de ce qui reste a examiner), donc aucune
    boucle infinie meme si le deck ne contient AUCUNE amelioration (arbitrage utilisateur du 27/10/2026 :
    rien ne s'attache alors, ce qui n'arrive jamais avec le deck de 5 cartes d'Iron Man -- hg019-hg022 sont 4
    UPGRADE, seule hg023 n'en est pas une).

    Rend la carte attachee, ou None si aucune amelioration n'a ete trouvee.

    ⚠⚠ PIEGE MOTEUR (mesure le 27/10/2026, premier mecanisme d'attache depuis UN DECK SIGNATURE du scenario) :
    `DeckSignatureDe` cree ce deck par `Deck2(metazombie.card, DeckType.AdditionalDeck, CardFace)` -- passer
    la CARTE du Metazombie comme `owner` fixe `deck.bind_card = metazombie.card` (deck.py:36). Or
    `CanAttach.bind_face` (can_attach.py:119) est une PROPRIETE CALCULEE : « la carte a laquelle je suis
    attachee » = « bind_card de la zone ou je me trouve actuellement » -- PAS un drapeau pose par une vraie
    attache. Toute carte simplement RANGEE dans le deck signature rapporte donc DEJA `bind_face == metazombie`,
    sans avoir jamais ete attachee ! `AttachTo2` commence par `if self.bind_face == face: ... return True`
    (court-circuit « deja attachee, replace juste dans la meme zone ») : appele directement depuis le deck
    signature, ce court-circuit se declenche a tort, renvoie `True`, et NE DEPLACE JAMAIS LA CARTE vers
    `metazombie.GetInventoryDeck()`. Aucune exception, aucun `ok=False` : juste une carte qui reste dans le
    deck signature en pretendant etre attachee. Prouve en comparant `trouvee.card.area` avant/apres
    `AttachTo2` (identique) ET `trouvee.bind_face` AVANT l'appel (deja egal a `metazombie`).
    Remede : sortir la carte du deck signature vers une zone NEUTRE (`world.area_processing`, modele
    `Puzzle.Engage` desengageant un sbire) AVANT d'appeler `AttachTo2`, pour que `bind_face` tombe a None et
    que le court-circuit ne se declenche plus."""
    from game.card.face.card_type import Attachment
    from game.operate.faces import Faces
    deck = DeckSignatureDe(effect, metazombie)
    limite = deck.GetSize()
    trouvee = None
    for _ in range(limite):
        carte = deck.GetTop()
        if carte is None:
            break
        if Attachment.IsType(carte):
            trouvee = carte
            break
        DefausserAuFondDuDeckSignature(effect, metazombie, carte)
    if trouvee is not None:
        Faces.MoveAllTo([trouvee], effect.world.area_processing, effect)
        trouvee.CastTo(Attachment).AttachTo2(metazombie, effect)
    # « shuffle the discarded cards into his signature deck » : remelange le deck (les cartes defaussees y
    # sont deja, au fond) pour qu'elles ne restent pas dans un ordre previsible.
    deck.Shuffle(effect)
    return trouvee


################################################################################
# Divers
def NombreDeJoueurs(effect: 'Effect') -> int:
    return max(1, len(Worlds.GetPlayers(effect)))


def PoserInfection(effect: 'Effect', joueur: 'Player', n: int = 1) -> None:
    """« Infection. When an attack from a Zombie or Metazombie enemy deals damage to your hero, place 1 Infection
    counter. » Le compteur vit sur l'identite (« a second health bar... tracked... next to your identity card »)."""
    Faces.PlaceCountersOn([joueur.GetIdentity()], n, 'infection', effect)


################################################################################
# « Zombie version of each chosen hero » (page 7, mise en place)
def NomHerosDe(joueur: 'Player') -> str:
    """Le nom du HEROS (pas de l'alter-ego, quelle que soit la forme courante) : c'est ce nom-la que les
    Metazombies et Fallen Heroes reprennent (« Zombie Captain America », pas « Zombie Steve Rogers »)."""
    from game.card.face.card_type import Hero
    identite = joueur.GetIdentity()
    for face in identite.card.printed_faces:
        if Hero.IsType(face):
            return face.name
    return identite.name


def HerosChoisis(effect: 'Effect') -> List[str]:
    return [NomHerosDe(j) for j in Worlds.GetPlayers(effect)]


def RetirerZombiesEtSurvivorsHomonymes(effect: 'Effect') -> List[str]:
    """Pour chaque heros choisi par les joueurs :
    - s'il a une version Metazombie dans le Horde deck, elle n'est simplement jamais generee
      (voir l'appel a `ConstruireLeHordeDeck` avec le resultat de cette fonction) ;
    - s'il a une version Metazombie dans Fallen Heroes (deja melangee au deck de rencontre par la mise en
      place generique du scenario), elle est mise de cote ;
    - s'il PARTAGE SON NOM avec un allie du Survivor deck (Wolverine, Blade), cet allie et son Trapped
      Survivor sont retires DU JEU (pas seulement mis de cote).
    Rend la liste des noms a exclure du Horde deck, a passer a `ConstruireLeHordeDeck`."""
    from game.operate.setup_cards import SetupCards
    noms = HerosChoisis(effect)

    for nom in noms:
        card_id = CARD_ID_FALLEN_PAR_HEROS.get(nom)
        if card_id is not None:
            SetupCards.SetAsideCards(effect, card_ids=[card_id])

    for nom in noms:
        id_allie = CARD_ID_SURVIVOR_ALLY_PAR_HEROS.get(nom)
        id_scheme = CARD_ID_SURVIVOR_SCHEME_PAR_HEROS.get(nom)
        if id_allie is None or id_scheme is None:
            continue
        # L'allie est mis de cote (Survivor deck) ; son Trapped Survivor, lui, est MELANGE AU DECK DE RENCONTRE
        # (livret p. 7, etape 6 : « The Hunger Core set (13 cards, with the remaining Trapped Survivors) ») avant
        # que ce Setup ne s'execute : on le cherche donc aux deux endroits.
        a_retirer = [f for f in Worlds.GetSetAsideAreaCards(effect)
                     if f.paper.card_id in (id_allie, id_scheme)]
        a_retirer += Worlds.GetEncounterDeck(effect).FindCards(card_ids=[id_scheme])
        if a_retirer:
            Faces.RemoveAllFromGame(a_retirer, effect)

    return [n for n in noms if n in CARD_ID_HORDE_PAR_HEROS]
