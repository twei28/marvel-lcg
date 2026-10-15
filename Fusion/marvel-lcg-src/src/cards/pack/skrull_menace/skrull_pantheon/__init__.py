from cards.pack import *

# ===========================================================================
# Scenario SKRULL PANTHEON (Skrull Menace, Kajislav) — helpers partages (sk170-183).
#
# Regles propres (insert p.14, « Skrull Deity » et « Alternation of Gods ») :
#  - Les mechants Kly'bn et Sl'gur't sont UNE SEULE carte DOUBLE FACE (Kly'bn d'un
#    cote, Sl'gur't de l'autre), par stade : `"villain": ["sk170a,sk170b", ...]`
#    (modele Typhoid Mary 60110a,60110b). Ils partagent leurs PV : c'est la meme
#    carte, donc le meme compteur de degats ; en vaincre un suffit.
#  - Le mechant collecte des JETONS DE FOI (compteur maison 'faith', declare dans
#    card_face.py). Les jetons ne peuvent pas etre retires tant que le complot
#    principal n'a pas avance au stade 2 : le seul retrait (Action de heros de
#    l'environnement Skrull Pantheon) n'existe qu'apres le stade 1, la regle est
#    donc tenue par construction.
#  - « Flip the villain » (traitrises, Nogor, Shapeless Wastes, complot 2B) : on
#    RETOURNE le mechant. Tous les attachements, cartes d'etat, cartes de boost et
#    autres elements associes sont defausses SAUF les jetons de foi et les degats ;
#    apres le retournement, on resout le « When Revealed » de la face visible
#    (`card.Flip(..., call_reveal=True)`).
#  - Apres la defaite d'un stade, le stade suivant arrive du MEME COTE (moteur :
#    `Scenario.AdvanceVillainStage` choisit la face de meme nom que le mechant
#    vaincu).
#  - L'environnement Skrull Pantheon (double face Stronghold / Destroyed) est mis de
#    cote a la mise en place (`set_aside` du scenario) et entre en jeu quand le
#    stade 1 du complot principal prend fin, face visible selon la facon dont il
#    prend fin.
# ===========================================================================

COMPTEUR_FOI = 'faith'
NOM_ENVIRONNEMENT = "Skrull Pantheon"
NOM_KLYBN = "Kly'bn"
NOM_SLGURT = "Sl'gur't"
ENSEMBLE_DARDVAN = "Dard'van Sect"
ENSEMBLE_PANTHEON = "Skrull Pantheon"


def EstTraitrise(face: 'CardFace') -> bool:
    """« treachery card » : type Treachery OU trait TREACHERY (decision utilisateur du
    15/10/2026 pour le coffret : les evenements de Lyja se melangent au deck rencontre)."""
    return Treachery.IsType(face) or face.HasTrait("TREACHERY")


def Divinite(effect: 'Effect') -> 'Villain|None':
    """Le mechant en jeu (la carte double face, quelle que soit la face visible)."""
    for nom in (NOM_KLYBN, NOM_SLGURT):
        mechant = Worlds.FindCardOnField(effect, name=nom, card_type=Villain)
        if mechant is not None:
            return mechant
    return None


def EstEnJeu(effect: 'Effect', nom: str) -> bool:
    """« Kly'bn is in play » / « Sl'gur't is in play » : la face VISIBLE du mechant porte ce nom
    (l'autre face n'est pas en jeu)."""
    return Worlds.FindCardOnField(effect, name=nom, card_type=Villain) is not None


def Foi(effect: 'Effect') -> int:
    """Nombre de jetons de foi sur le mechant (0 sans mechant)."""
    mechant = Divinite(effect)
    return mechant.GetCounters(COMPTEUR_FOI) if mechant is not None else 0


def PoserFoi(effect: 'Effect', nombre: int=1) -> None:
    mechant = Divinite(effect)
    if mechant is not None and nombre > 0:
        Faces.PlaceCountersOn([mechant], nombre, COMPTEUR_FOI, effect)


def RetirerFoi(effect: 'Effect', nombre: int=1) -> None:
    mechant = Divinite(effect)
    if mechant is not None and nombre > 0:
        Faces.RemoveCountersOn([mechant], nombre, COMPTEUR_FOI, effect)


def DefausserElementsAssocies(effect: 'Effect', mechant: 'CardFace') -> None:
    """Retournement : tous les attachements, cartes d'etat, cartes de boost et autres elements
    associes au mechant sont defausses, SAUF les jetons de foi et les degats (insert p.14). Les
    compteurs et les degats sont des composants de la CARTE : ils restent d'eux-memes."""
    attaches = list(mechant.GetAttachedAttachments()) + list(mechant.GetAttachedUpgrades())
    statuts = list(mechant.card.components.status.GetDeck().GetAll())
    boosts = list(mechant.card.components.boostable.GetDeck().GetAll())
    for lot in (attaches, statuts, boosts):
        if lot:
            Faces.DiscardAll(lot, effect)


def RetournerLeMechant(effect: 'Effect') -> bool:
    """« Flip the villain » : defausse les elements associes, retourne la carte, puis la face
    d'arrivee resout son « When Revealed » (`call_reveal=True`, comme le retournement d'un complot).
    Rend True si le retournement a eu lieu."""
    mechant = Divinite(effect)
    if mechant is None or effect.world.is_game_over:
        return False
    DefausserElementsAssocies(effect, mechant)
    return mechant.card.Flip(effect)


def JoueursDansLOrdre(effect: 'Effect') -> List['Player']:
    """Les joueurs encore en lice, le premier joueur en tete (« in player order »)."""
    return [p for p in effect.world.players if not p.is_eliminated]


def DistribuerEnOrdre(effect: 'Effect', cartes: Sequence['CardFace']) -> None:
    """« Deal the players each X card as a facedown encounter card in player order » : les cartes
    sont donnees UNE A UNE, en commencant par le premier joueur, en repartant du premier quand tous
    en ont recu (lecture retenue : voir defs/pantheon_questions.md)."""
    joueurs = JoueursDansLOrdre(effect)
    if not joueurs:
        return
    for rang, face in enumerate(cartes):
        if effect.world.is_game_over:
            return
        joueurs[rang % len(joueurs)].DealEncounterCard(face, effect)


def ReponseFoi(traitrises: bool) -> 'Ability':
    """Reponse forcee commune aux six faces du mechant : « After resolving step one of the villain
    phase, discard the top card of the encounter deck for each faith counter on <nom>. Deal the
    players each [non-]treachery card discarded this way as a facedown encounter card in player
    order. » `traitrises` : False pour Kly'bn (non-traitrises), True pour Sl'gur't (traitrises)."""

    def distribuer(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        nombre = effect.this.GetCounters(COMPTEUR_FOI)
        if nombre <= 0:
            return
        defaussees = Worlds.DiscardEncounterCards(nombre, effect)
        retenues = [f for f in defaussees if EstTraitrise(f) == traitrises]
        DistribuerEnOrdre(effect, retenues)

    return AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, distribuer)


def RevelationDuMechant(avec_tenace: bool) -> 'Ability':
    """« When Revealed : Place 1 faith counter on <nom> [and give him/her a tough status card]. »"""

    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this
        Faces.PlaceCountersOn([this], 1, COMPTEUR_FOI, effect)
        if avec_tenace:
            Faces.GiveStatus([this], "Tough", effect)

    return AbilityFactory.WhenThisRevealed(None, reveler)


def ActionRetirerFoi(cout: 'Cost') -> 'Ability':
    """« Hero Action: Spend ... → remove 1 faith counter from the villain. » (les deux faces de
    l'environnement). Offerte seulement s'il reste un jeton de foi a retirer."""

    def il_reste_de_la_foi(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return Foi(effect) > 0

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        RetirerFoi(effect, 1)

    return AbilityFactory.WhenInYourPlayTurn(
        AbilityType.HeroAction, retirer, conditions=[il_reste_de_la_foi],
    ).SetCost(cout)


def EnvironnementMisDeCote(effect: 'Effect') -> 'CardFace|None':
    """L'environnement Skrull Pantheon mis de cote a la mise en place (`set_aside` du scenario)."""
    for face in Worlds.AsideDeck(effect).Get(True):
        if Environment.IsType(face) and face.IsName(NOM_ENVIRONNEMENT):
            return face
    return None


def MettreLEnvironnementEnJeu(effect: 'Effect', detruit: bool) -> 'CardFace|None':
    """« Put the set-aside Skrull Pantheon environment into play, DESTROYED / STRONGHOLD side faceup. »
    La carte entre face Stronghold (face A imprimee) ; on la retourne pour la face Destroyed."""
    env = EnvironnementMisDeCote(effect)
    if env is None:
        return None
    env.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)
    if detruit and env.IsInPlay():
        env.card.Flip(effect)
    return env


def AvancerAuStade2FaceB(effect: 'Effect', scheme: 'MainScheme') -> None:
    """« Advance to stage 2B » : le complot saute la face A du stade 2 (donc son « When Revealed »,
    la recherche de Strengthen the Faith) et arrive directement sur la face B. On retourne la carte
    du stade 2 dans le paquet des complots, puis on avance vers SA face B."""
    suivant = effect.world.main_schemes_deck.FindCard(CardFinder(stage=2), card_type=MainScheme)
    if suivant is None:
        scheme.Advance(None, effect)
        return
    suivant.card.Flip(effect, call_reveal=False)
    scheme.Advance(suivant.card.face, effect)
