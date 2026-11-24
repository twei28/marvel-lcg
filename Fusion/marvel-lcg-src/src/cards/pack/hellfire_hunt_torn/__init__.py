from cards.pack import *

# ===========================================================================
# Pack HELLFIRE HUNT - SCENARIO 4 « TORN » (campagne Hellfire Hunt, « MC Custom Content By: Dipsome »), 01/11/2026.
# Prefixe `hf` (deja declare : tools/prefixes_fanmade.json), set 244. Module PLAT : `cards.pack.hellfire_hunt_torn.<card_id>`
# (modele : hellfire_hunt_white_queen). Tout helper appele par une carte vit ICI (NameError avale par le moteur sinon, lecon hk005).
#
# card_id : hf501-hf510 = scenario (500 + numero n/10 du scan : 501 = Emma Frost A, 502 = Emma Frost B, 503 = complot 1A/1B, 504 = Nova's Psychic
# Puppetry, 505-510 = rencontre), hf341-hf348 = module Negasonic Teenage Warhead, hf351-hf358 = module Immensity (340/350 + numero du scan ;
# les exemplaires d'une meme carte ont chacun leur card_id, comme Perfection).
#
# LE SCENARIO EN UNE PHRASE : Emma Frost est UN vilain a quatre faces (A1/A2 en standard, B1/B2 en expert). La face « active » (1) a des PV ; quand
# elle serait vaincue elle se RETOURNE a la place (et 5 menaces partent de chaque manigance) sur la face « retournee » (2) a PV INFINIS ; apres la
# phase du vilain elle revient sur la face active, PV remis a leurs valeurs imprimees. Elle ne peut donc jamais etre vaincue : on gagne en retirant
# toute la menace de Nova's Psychic Puppetry (face FRAGMENT).
# LE DECK HELLFIRE : les sbires ELITE HELLFIRE sont retires du deck de rencontre pour former un deck de TABLE a part, avec sa propre defausse
# (`DeckHellfire`) ; on les y remet « sans penalite » quand il est vide.
# ===========================================================================

NOM_EMMA = "Emma Frost"
NOM_WHITE_QUEEN = "White Queen"
NOM_CASSANDRA = "Cassandra Nova"
NOM_PUPPETRY = "Nova's Psychic Puppetry"
NOM_CLOAK = "Cassandra's Telepathic Cloak"
HELLFIRE = "HELLFIRE"
ELITE = "ELITE"
PSIONIQUE = "PSIONIC"
ILLUSION = "ILLUSION"


# ---------------------------------------------------------------------------------------------------------------- les faces
def EmmaFrost(effect: 'Effect') -> 'Villain|None':
    """Le VILAIN Emma Frost en jeu."""
    for v in Worlds.GetVillains(effect):
        if v.IsName(NOM_EMMA):
            return v
    return None


def EstSbireEliteHellfire(face: 'CardFace|None') -> bool:
    return face is not None and Minion.IsType(face) and face.HasTrait(ELITE) and face.HasTrait(HELLFIRE)


def EstSbireHellfire(face: 'CardFace|None') -> bool:
    return face is not None and Minion.IsType(face) and face.HasTrait(HELLFIRE)


# ---------------------------------------------------------------------------------------------------------------- le deck Hellfire (E5)
def DeckHellfire(effect: 'Effect') -> 'Tuple[Deck, Deck]':
    """(deck, defausse) du Hellfire deck de cette partie. Deck de TABLE (scenario proprietaire), cree A LA DEMANDE, un seul par partie
    (modele : `cards.pack.hellfire_hunt.RecruitedMutants`, meme mecanisme `additional_decks` du moteur)."""
    from game.deck.deck import Deck2
    from game.deck.deck_type import DeckType
    from game.card.face.card_face import CardFace

    monde = effect.world
    etat = getattr(monde, "hf_hellfire", None)
    if etat is None:
        deck = Deck2(monde.scenario, DeckType.AdditionalDeck, CardFace)
        defausse = Deck2(monde.scenario, DeckType.AdditionalDiscardPile, CardFace)
        deck.BindDiscardPile(defausse, lambda deck, effect: None)     # « no penalty » : rien apres le remelange
        monde.additional_decks.append(deck)
        monde.additional_discard_piles.append(defausse)
        etat = (deck, defausse)
        monde.hf_hellfire = etat
    return etat


def VersLeDeckHellfire(effect: 'Effect', faces: 'Sequence[CardFace]') -> None:
    """Met ces cartes dans le Hellfire deck ; defaussees ou vaincues, elles iront dans la defausse Hellfire (`card.bind_discard_pile`),
    et non dans celle du deck de rencontre. Ne melange pas."""
    deck, defausse = DeckHellfire(effect)
    faces = list(faces)
    if faces:
        Faces.MoveAllTo(faces, deck, effect)
    for face in faces:
        face.card.bind_discard_pile = defausse


def ConstruireLeDeckHellfire(effect: 'Effect') -> 'List[CardFace]':
    """Mise en place (complot 1A) : « Shuffle every ELITE, HELLFIRE minion to create the Hellfire deck and set it next to the encounter deck. »
    Les sbires ELITE HELLFIRE sont CHERCHES dans le deck de rencontre (modules compris), puis melanges ensemble."""
    elites = [f for f in Worlds.GetEncounterDeckCards(effect) if EstSbireEliteHellfire(f)]
    VersLeDeckHellfire(effect, elites)
    deck, _ = DeckHellfire(effect)
    deck.Shuffle(effect)
    return elites


def RemelangerLeDeckHellfireSiVide(effect: 'Effect') -> None:
    """« If the Hellfire deck is ever empty, shuffle the Hellfire discard pile into the Hellfire deck. There is no penalty for doing this. »"""
    deck, defausse = DeckHellfire(effect)
    if deck.GetSize() == 0 and defausse.GetSize() > 0:
        Faces.MoveAllTo(list(defausse.Get(True)), deck, effect)
        deck.Shuffle(effect)


def DessusDuDeckHellfire(effect: 'Effect') -> 'CardFace|None':
    RemelangerLeDeckHellfireSiVide(effect)
    deck, _ = DeckHellfire(effect)
    return deck.GetTop()


def RevelerDuDeckHellfire(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« reveal the top card of the Hellfire deck » : le sbire est revele devant `joueur` (engage avec lui). Rend la carte, ou None si le
    deck ET sa defausse sont vides."""
    face = DessusDuDeckHellfire(effect)
    if face is None:
        return None
    face.Reveal(joueur, effect)
    return face


def CartesDuHellfire(effect: 'Effect') -> 'List[CardFace]':
    """Tout ce que le Hellfire deck et sa defausse contiennent (pour un « find »)."""
    etat = getattr(effect.world, "hf_hellfire", None)       # jamais cree par une simple recherche (scenario 5 : Immensity sans Hellfire deck)
    if etat is None:
        return []
    return list(etat[0].Get(True)) + list(etat[1].Get(True))


# ---------------------------------------------------------------------------------------------------------------- les joueurs
def JoueursDansLOrdre(effect: 'Effect') -> 'List[Player]':
    """« in player order » : le premier joueur d'abord, puis dans l'ordre des sieges."""
    joueurs = list(Worlds.GetPlayers(effect))
    premier = Worlds.GetFirstPlayer(effect)
    if premier in joueurs:
        i = joueurs.index(premier)
        joueurs = joueurs[i:] + joueurs[:i]
    return joueurs


def SansSbireEngage(joueur: 'Player') -> bool:
    """« each player with no engaged minions »."""
    return len(joueur.GetEngagedMinions()) == 0


def DonnerUneCarteFaceCachee(effect: 'Effect', joueurs: 'Sequence[Player]|None'=None, nombre: int=1) -> None:
    """« deal each player a facedown encounter card »."""
    for joueur in (joueurs if joueurs is not None else JoueursDansLOrdre(effect)):
        joueur.DealEncounterCards(nombre, effect)


# ---------------------------------------------------------------------------------------------------------------- Emma Frost (E6)
def InterruptionDefaiteEmma() -> 'Ability':
    """Faces actives (A1, B1) : « Forced Interrupt : When Emma Frost would be defeated, remove 5 threat from each scheme in play, and flip this card
    instead. » La defaite n'a PAS lieu (`SetBeInstead`) ; les degats restent sur la carte, que la face retournee (PV infinis) absorbe.
    Modele : 16080a Collector (`WhenUnitWouldBeDefeated` + `RemoveThreatFromSchemes` + `card.Flip`)."""
    def vaincue(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Villain)
        message.SetBeInstead(effect)
        this.RemoveThreatFromSchemes("EachScheme", 5, effect)
        this.card.Flip(effect)

    return AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, "This", vaincue)


def RetourSurLaFaceActive() -> 'Ability':
    """Faces retournees (A2, B2) : « Forced Response : After the end of the villain phase, flip this card, then set Emma Frost's hit point dial to
    her printed hit points. » Le moteur remet les PV au retournement depuis une face a PV infinis (`can_health.py OnFlip` : `ResetHealth`)."""
    def fin_de_phase(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Villain)
        this.card.Flip(effect)

    return AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", fin_de_phase)


def MenaceSurChaqueManigance(effect: 'Effect', nombre: int) -> None:
    """« place N threat on each scheme » (complot principal ET manigances annexes)."""
    for _ in range(nombre):
        effect.this.PlaceThreatOnSchemes("EachScheme", 1, effect)


# ---------------------------------------------------------------------------------------------------------------- Nova's Psychic Puppetry
def ReponseSbireEliteVaincu() -> 'Ability':
    """Deux faces : « Forced Response : After an ELITE, HELLFIRE minion is defeated, remove 5 threat from another side scheme. Otherwise, remove 5
    threat from here. » Le joueur qui a vaincu le sbire (a defaut le premier joueur) choisit l'AUTRE manigance annexe ; s'il n'y en a pas, la menace
    part d'ici. Modele : sk229 / sk040 (`AskChooseFace`), `WhenUnitBeDefeated(ForcedResponse, finder, op)`."""
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(SchemeSide2)
        autres = [s for s in Worlds.GetSideSchemes(effect) if s is not this]
        if autres:
            joueur = message.defeating_player or Worlds.GetFirstPlayer(effect)
            cible = autres[0] if len(autres) == 1 else joueur.AskChooseFace(autres, effect, not_move=True)
            this.RemoveThreatFromSchemes([cible], 5, effect)
        else:
            this.RemoveThreatFromSchemes([this], 5, effect)

    return AbilityFactory.WhenUnitBeDefeated(
        AbilityType.ForcedResponse, CardFinder2(HELLFIRE, Minion), vaincu,
        conditions=[lambda effect, message: message.trigger.HasTrait(ELITE)])


# ---------------------------------------------------------------------------------------------------------------- modules Negasonic / Immensity
def EpuiserUnSoutienOuUneAmelioration(effect: 'Effect', joueur: 'Player|None') -> 'CardFace|None':
    """« exhaust a support or upgrade you control, if able » : un soutien ou une amelioration PRET que ce joueur controle (ameliorations des
    allies comprises, `GetControlUpgrade`). Le joueur choisit s'il y en a plusieurs ; rend la carte epuisee, ou None si aucune."""
    if joueur is None:
        return None
    candidats = [f for f in list(joueur.supports.Get()) + list(joueur.GetControlUpgrade()) if f.IsReady()]
    if not candidats:
        return None
    choisie = candidats[0] if len(candidats) == 1 else joueur.AskChooseFace(candidats, effect, not_move=True)
    if choisie is None:
        return None
    Faces.ExhaustAll([choisie], effect)
    return choisie


def ChercherCassandra(effect: 'Effect') -> 'CardFace|None':
    """« find Cassandra Nova » : en jeu, ou dans le deck de rencontre, sa defausse, la zone mise de cote, le Hellfire deck ou sa defausse."""
    for face in Worlds.GetOnFieldMinions(effect):
        if face.IsName(NOM_CASSANDRA):
            return face
    candidats = (list(Worlds.GetEncounterDeckCards(effect)) + list(Worlds.GetEncounterDiscardPileCards(effect))
                 + list(Worlds.GetSetAsideAreaCards(effect)) + CartesDuHellfire(effect))
    for face in candidats:
        if Minion.IsType(face) and face.IsName(NOM_CASSANDRA):
            return face
    return None


def ChercherLeManteau(effect: 'Effect') -> 'CardFace|None':
    """« find the Cassandra's Telepathic Cloak attachment » : deck de rencontre, sa defausse, la zone mise de cote."""
    candidats = (list(Worlds.GetEncounterDeckCards(effect)) + list(Worlds.GetEncounterDiscardPileCards(effect))
                 + list(Worlds.GetSetAsideAreaCards(effect)))
    for face in candidats:
        if Attachment.IsType(face) and face.IsName(NOM_CLOAK):
            return face
    return None


# ---------------------------------------------------------------------------------------------------------------- carnet de campagne (victoire du scenario 4)
def ReleveTorn(effect: 'Effect', message: 'Message.WhenGameOver') -> 'Dict[str, Any]':
    """Livret p.14, VICTOIRE du scenario 4 : « Shuffle each RECRUITED ally in each player's deck and discard pile into the Recruited Mutants deck. Record the name of
    each ... ally in the Recruited Mutants Deck as "Recruited" in the campaign log. » Le releve COMMUN (`cards.pack.hellfire_hunt.campaign.Releve`) ne regarde que les
    allies EN JEU ou dans la pile de victoire ; ici on y ajoute tout allie de campagne qui n'est PLUS dans la zone « mise de cote » (deck, defausse, main, deck et defausse
    Recruited Mutants) : un allie sorti de la zone mise de cote par une manigance POTENTIAL ALLY n'y retourne jamais."""
    from cards.pack.hellfire_hunt import campaign as hc
    updates = hc.Releve(4, effect, message)
    if not updates:
        return updates
    recrutes = [i for i in str(updates.get(hc.CLE_RECRUTES, '')).split(hc.SEP) if i]
    aside = effect.world.aside_deck
    for card_id in hc.ALLIES:
        if card_id in recrutes:
            continue
        for objet in effect.world.object_manager.card_dict.values():
            face = objet.face
            if face is not None and face.paper.card_id == card_id and face.card.area is not aside:
                recrutes.append(card_id)
                break
    updates[hc.CLE_RECRUTES] = hc.SEP.join(recrutes)
    return updates
