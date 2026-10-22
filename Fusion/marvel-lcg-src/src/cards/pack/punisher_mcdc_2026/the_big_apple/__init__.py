from ..commun import *
from ..campaign import CampaignSetup, NoterLeLieuDeLaDernierePiste
from ..leads_the_big_apple import CreerPaquetPistes, RevelerPiste, PistesEnVictoire, Joueur, ControlePar

# Set The Big Apple (pack MC×DC 2026) : scenario 1, la ville. Environnements The City / Never Sleeps, complots Gang War / Silence the City /
# Gunrunner's Warehouse, attachement Gunrunner, sbires et cartes de rencontre.
#
# Vocabulaire : « le CAPO d'une rangee » = le vilain de la zone de jeu de cette rangee ; les zones : indice 0 = zone de depart, puis la zone
# COMMUNE (manigances, environnements de la ville), puis une zone par rangee (`Ville.Installer`).

GRILLE_DES_LIEUX = [["pu030", "pu031", "pu032"], ["pu033", "pu034", "pu035"], ["pu036", "pu037", "pu038"]]
CASE_DE_DEPART = (1, 1)   # Midtown


def TousLesJoueurs(effect: 'Effect') -> 'List[Player]':
    """TOUS les joueurs, quelle que soit leur zone (`Worlds.GetPlayers` filtre par la zone de la carte qui resout : un complot de la zone commune
    n'y voit AUCUN joueur)."""
    return [j for j in effect.world.const_players if j.area_hero.GetSize() > 0]


def LeVilain(effect: 'Effect', joueur: 'Player') -> 'Villain|None':
    """« the villain » d'un joueur dans la ville (R6) : le CAPO de SA zone ; hors ville (banc de test), le vilain courant."""
    zone = joueur.GetIdentity().card.GetGameArea()
    for v in Worlds.GetAllVillains(effect):
        if v.card.GetGameArea() is zone:
            return v
    return Worlds.FindVillain(effect)


def LieuDeLaPiste(card_id_piste: str) -> str:
    """Le lieu d'une piste : pu039 -> pu030 ... pu047 -> pu038 (meme numero que dans le titre)."""
    return "pu%03d" % (int(card_id_piste[2:]) - 9)


def MisDeCote(effect: 'Effect', card_id: str) -> 'CardFace|None':
    """La carte `card_id` dans la zone de mise de cote du scenario."""
    for face in Worlds.GetSetAsideAreaCards(effect):
        if face.paper.card_id == card_id:
            return face
    return None


def CapoDe(effect: 'Effect', zone: 'GameArea') -> 'Villain|None':
    for v in Worlds.GetVillains(effect):
        if v.card.game_area is zone and v.HasTrait("CAPO"):
            return v
    return None


def MettreEnPlaceLaVille(effect: 'Effect', rangees: int=3) -> 'List[Villain]':
    """Gang War 1A, Setup : « Place the 9 locations in numerical order in a 3x3 grid. Place one chosen CAPO villain next to each row. Create
    the 9-card LEADS deck. Reveal The City and Never Sleeps environments. Each player reveals a card from the LEADS deck. »
    Rend les CAPO en jeu, de la rangee 0 a la derniere."""
    world = effect.world
    this = effect.this
    premier = Worlds.GetFirstPlayer(effect)

    commune = world.CreateCommonGameArea()
    zones = {ligne: world.CreateGameArea() for ligne in range(rangees)}

    cases = {}
    for ligne, rangee in enumerate(GRILLE_DES_LIEUX[:rangees]):
        for colonne, card_id in enumerate(rangee):
            lieu = MisDeCote(effect, card_id)
            if lieu is None:
                continue
            lieu.PutIntoPlay(premier, effect)
            zones[ligne].AddCard(lieu.card)
            cases[(ligne, colonne)] = lieu

    for card_id in ("pu005", "pu006"):
        environnement = MisDeCote(effect, card_id)
        if environnement is not None:
            environnement.PutIntoPlay(premier, effect)
            commune.AddCard(environnement.card)
    commune.AddCard(this.card)

    # « Place one chosen CAPO villain next to each row » : trois tires au hasard parmi ceux mis de cote (face A en standard, B en expert :
    # le scenario ne met de cote que la bonne face). Les autres restent dans le deck de mechants : « Reveal a random CAPO villain from the
    # set-aside area » (3A) en tire un.
    candidats = [f.CastTo(Villain) for f in Worlds.GetSetAsideAreaCards(effect, CardFinder(card_type=Villain)) if f.HasTrait("CAPO")]
    Villains.BuildVillainDeck(candidats, effect)
    capos: List['Villain'] = []
    for ligne in range(rangees):
        capo = Villains.RevealNextVillain(premier, effect)
        if capo is not None:
            zones[ligne].AddCard(capo.card)
            capos.append(capo)
    Villains.SetRule(effect, Villains.Rule(the_villain="Leftmost", player_cards="TheVillain"))

    if capos:
        CreerPaquetPistes(effect, capos[0])
    Ville.Installer(world, cases, zones, CASE_DE_DEPART)
    for joueur in TousLesJoueurs(effect):
        RevelerPiste(effect, joueur)
    return capos


################################################################################
# M5 : cartes liees aux lieux (22/10/2026)
def ChoisirLieuInoccupe(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« an unoccupied location » : le JOUEUR concerne choisit parmi les lieux sans joueur (aucun : None)."""
    libres = Ville.LieuxInoccupes(effect)
    if not libres:
        return None
    return libres[0] if len(libres) == 1 else joueur.AskChooseFace(libres, effect)


def AttacherAuLieuInoccupe(effect: 'Effect', sbire: 'CardFace', joueur: 'Player|None') -> bool:
    """« attach <sbire> to an unoccupied location, if able » (Overdrive, Muse, Screwball) : rien si aucun lieu libre ou plus de ville."""
    if joueur is None:
        return False
    return Ville.AttacherSbire(effect, sbire, ChoisirLieuInoccupe(effect, joueur))


def SbireEngagePar(sbire: 'CardFace') -> 'Player|None':
    try:
        return sbire.CastTo(Minion).engaged_player
    except AssertionError:
        return None


def EngageQuandOnEntreDansSonLieu() -> 'Ability':
    """« Forced Interrupt : When a player enters <le sbire>'s location, he engages them. » Capacite portee par le sbire ATTACHE, donc hors jeu
    (`NoOutOfPlayLimit`) : le joueur qui arrive est celui du message, le lieu celui qui porte le sbire."""
    def lieu_du_sbire(effect: 'Effect', message: 'Message.WhenPlayerWouldEnterLocation') -> bool:
        return Ville.Hote(effect.this) is message.lieu

    def engage(effect: 'Effect', message: 'Message.WhenPlayerWouldEnterLocation') -> None:
        Ville.DegagerSbire(effect, effect.this, message.GetToPlayer())

    return Ability(AbilityType.ForcedInterrupt, Message.WhenPlayerWouldEnterLocation, [lieu_du_sbire], engage).NoOutOfPlayLimit().NoGameAreaLimit()


def AuLieuDeLAttachement(message_lieu: 'Callable[[Message2], CardFace|None]') -> 'Callable[[Effect, Message2], bool]':
    """Condition : le lieu du message est celui qui PORTE cet attachement (`bind_face`)."""
    def condition(effect: 'Effect', message: 'Message2') -> bool:
        hote = getattr(effect.this, 'bind_face', None)
        return hote is not None and message_lieu(message) is hote
    return condition
