"""Campagne « The Galaxy's Most Wanted » : mise en place et releve du carnet.

Regles du livret officiel mc16 : pages 4 et 5 pour les regles generales, puis
les encarts CAMPAIGN INSTRUCTIONS des pages 8, 10, 12, 14-15 et 18.

Deux choses la distinguent des cinq autres campagnes du jeu :

  * le CHASSEUR DE TETES badoon, melange au deck rencontre a CHAQUE scenario.
    Chaque fois qu'on le vainc, la chasse s'intensifie : le livret ajoute une
    carte de plus au scenario suivant, par paliers cumulatifs. C'est la seule
    mecanique du jeu ou BIEN JOUER rend la suite plus dure.
  * les UNITES. Chaque victoire en rapporte, elles s'accumulent au carnet et se
    depensent au Marche entre deux scenarios. Le comptage vit ici ; la depense
    vit dans l'ecran des campagnes.

Le releve suit la regle des quatre autres collecteurs : on ne consigne QUE ce
que le moteur sait constater.
"""
from . import *
from cards.pack.mts.campaign import ActiveMainSchemeStartswith, FaceExists, WriteCampaignLogAtGameOver
from cards.pack.gmw.collector_1 import GetTheCollection

# Le minion qui poursuit les joueurs d'un scenario a l'autre.
CHASSEUR = '16183'

# Les cinq scenarios, dans l'ordre du livret. Sert aux cles du carnet.
SCENARIOS = ['Brotherhood of Badoon', 'Infiltrate the Museum', 'Escape the Museum',
             'Nebula', 'Ronan the Accuser']

# Les memes, par ID de scenario de la campagne (`data/campagnes/gmw.json`) : c'est
# l'estampille que le panneau de recompenses attend sur le carnet sortant.
IDS_SCENARIOS = ['brotherhood_of_badoon', 'infiltrate_the_museum', 'escape_the_museum',
                 'nebula', 'ronan']

# Palier de marques « Headhunter Defeated? » -> carte ajoutee au deck rencontre.
# Le livret les CUMULE : a 3 marques, les trois premieres sont la.
RENFORTS = [(1, '16184'),   # On the Hunt (traitrise)
            (2, '16185'),   # Dead to Rights (traitrise)
            (3, '16186'),   # Headhunter's Henchman (minion)
            (4, '16187')]   # Fugitive Recovery (manigance annexe)

# La manigance de campagne revelee a la mise en place, une par scenario.
# « use the reverse side for expert mode » : on ne choisit PAS la face ici, la
# carte s'en charge (AbilityFactoryExpert.StandardModeOnly / ExpertModeOnly).
MANIGANCES = {1: '16178a,16178b', 2: '16179a,16179b', 3: '16180a,16180b',
              4: '16181a,16181b', 5: '16182a,16182b'}

# Scenario 4 : chaque artefact rapporte au 3 revient, et se paie.
#
# CORRECTIF DU 19/09/2026, trouve par les epreuves de campagne. Le carnet
# officiel (mc16, page 22) intitule la case « Galactic Artifacts Side Schemes
# in the Victory Display » : ce sont les quatre MANIGANCES ANNEXES ci-dessous,
# et elles ne portent AUCUN trait. Le releve filtrait sur un trait
# « GALACTIC ARTIFACT » qui n'existe sur aucune carte du jeu — les seules
# cartes traitees du set sont les ameliorations 16122-16126, dont le trait est
# « ARTIFACT » et qui ne sont pas concernees. Resultat : la case n'etait
# JAMAIS remplie, aucun artefact ne revenait au scenario 4, et la prime en
# unites du scenario 3 ne tombait jamais. On identifie desormais par card_id.
ARTEFACTS = {'16127': 'Hujahdarian Monarch Egg',
             '16128': 'Magical Teapot',
             '16129': "Philosopher's Stone",
             '16130': 'Crystal Ball'}

# L'ancienne graphie fautive (« Hujadarian », sans le h du milieu) a pu etre
# saisie a la main dans un carnet existant : on la relit encore.
ALIAS_ARTEFACTS = {'hujadarian monarch egg': '16127'}


def CodeArtefact(nom: str) -> 'str|None':
    """Le card_id d'un artefact designe par son nom au carnet."""
    cible = (nom or '').strip().lower()
    for code, officiel in ARTEFACTS.items():
        if officiel.lower() == cible:
            return code
    return ALIAS_ARTEFACTS.get(cible)

SEPARATEUR = ';'


# ---------------------------------------------------------------- lectures --
def _liste(valeur: str) -> 'List[str]':
    return [x for x in (valeur or '').split(SEPARATEUR) if x]


def _entier(effect: 'Effect', cle: str) -> int:
    try:
        return int(CampaignLog.GetStrInternal(cle, effect) or 0)
    except ValueError:
        return 0


def MarquesDuChasseur(effect: 'Effect') -> int:
    """Combien de fois le Chasseur de tetes a deja ete vaincu."""
    return sum(1 for nom in SCENARIOS
               if CampaignLog.GetStrInternal(f'Headhunter Defeated: {nom}', effect))


def CartesDeLaCollection(effect: 'Effect') -> 'List[CardFace]':
    """La Collection est un deck de scenario nomme, pas une pile sous une carte."""
    collection = GetTheCollection(effect)
    return list(collection.deck.GetAll()) if collection else []


def CompteursEsquive(effect: 'Effect') -> int:
    return sum(f.GetCounters('evasion') for f in Worlds.FindCardsOnField(effect, card_type=Environment))


# ------------------------------------------------------------ mise en place --
def RevelerLaManiganceDeCampagne(level: int) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(MANIGANCES[level], None, effect.world)
        card.face.Reveal(Worlds.GetFirstPlayer(effect), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def MelangerLeChasseurEtSesRenforts() -> 'Ability':
    """Le Chasseur, puis ce que ses defaites precedentes ont attire."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        marques = MarquesDuChasseur(effect)
        encounter_deck = Worlds.GetEncounterDeck(effect)
        for card_id in [CHASSEUR] + [cid for palier, cid in RENFORTS if marques >= palier]:
            card = CardFactory.GenerateCard(card_id, None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
        Unused(encounter_deck)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def RetirerLesCartesDeLaCollection() -> 'Ability':
    """Scenario 3 : ce que le musee vous a pris ne revient pas.

    Livret p.12 : « Each player must search their deck, discard pile, and hand
    for each of their cards recorded in the "Cards in The Collection" section
    of the campaign log, then remove those cards from the game. Each player
    draws up to their hand size. »
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            ids = _liste(CampaignLog.GetStrByPlayer('Collection Cards', player.player_id, effect))
            if not ids:
                continue
            a_retirer: List['CardFace'] = []
            for zone in (player.player_deck, player.discard_pile, player.hand_cards):
                a_retirer += [f for f in zone.GetAll() if f.paper.card_id in ids]
            if a_retirer:
                Faces.RemoveAllFromGame(a_retirer, effect)
            player.DrawUp('Max', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def RemelangerLesArtefacts() -> 'Ability':
    """Scenario 4 : chaque artefact laisse au musee revient, et se paie.

    Livret p.14, mot pour mot : « Shuffle each Galactic Artifacts side scheme
    recorded in the "Galactic Artifacts Side Schemes in the Victory Display"
    section of the campaign log into the encounter deck. Perform the following
    for each specified side scheme shuffled in this way. »

    CORRECTIF DU 19/09/2026 : le remelange ANNONCE PAR LE NOM DE LA FONCTION
    n'etait pas fait. Seules les quatre consequences se posaient, et les
    manigances elles-memes ne revenaient jamais dans le deck rencontre — alors
    que c'est la punition principale : ce qu'on a emporte du musee vous
    repoursuit chez Nebula.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        from cards.pack.gmw.nebula import FindNebulaShip
        gardes = _liste(CampaignLog.GetStrInternal('Galactic Artifacts in Victory Display', effect))
        villains = Worlds.GetAllVillains(effect.world)
        for nom in gardes:
            code = CodeArtefact(nom)
            if code:
                carte = CardFactory.GenerateCard(code, None, effect.world)
                Faces.ShuffleAllTo([carte.face], 'EncounterDeck', effect)
            if code == '16127':
                # « Place 1 evasion counter on Nebula's Ship » : sur LE
                # vaisseau, pas sur un environnement quelconque.
                ship = FindNebulaShip(effect)
                if ship:
                    ship.PlaceCountersInternal(1, 'evasion', effect)
            elif code == '16128':
                Worlds.GetFirstPlayer(effect).DealEncounterCards(1, effect)
            elif code == '16129':
                encounter_deck = Worlds.GetEncounterDeck(effect)
                for villain in villains:
                    top = encounter_deck.GetTop()
                    if top:
                        villain.GiveBoostCard(top, effect)
                    break
            elif code == '16130':
                if villains:
                    Faces.GiveStatus([villains[0]], 'Tough', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def ChercherDansLeDeckRencontre(effect: 'Effect', card_id: str) -> 'CardFace':
    """Un exemplaire d'une carte, pris au deck rencontre ou a sa defausse.

    CORRECTIF DU 19/09/2026 : le scenario 5 disait « search the encounter deck
    and discard pile for one copy of X », et le code FABRIQUAIT une carte de
    plus. Le deck gardait donc ses trois « You Stand Accused! » et le joueur en
    recevait un quatrieme, sorti de nulle part. On prend maintenant un
    exemplaire existant ; on n'en fabrique un que s'il n'en reste aucun, ce qui
    ne peut arriver qu'avec un deck deja entame.
    """
    for pile in (Worlds.GetEncounterDeck(effect), Worlds.GetEncounterDiscardPile(effect)):
        for face in pile.GetAll():
            if face.paper.card_id.startswith(card_id):
                return face
    return CardFactory.GenerateCard(card_id, None, effect.world).face


def PoserLaSuiteDeRonan() -> 'Ability':
    """Scenario 5 : la Pierre du Pouvoir se paie, et l'esquive aussi (p.18)."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        porteur = CampaignLog.GetStrInternal('Power Stone Control', effect)
        if porteur:
            for player in Worlds.GetPlayers(effect):
                identity = player.GetIdentity()
                if identity and (NomDeHeros(identity) == porteur):
                    face = ChercherDansLeDeckRencontre(effect, '16116')
                    player.DealEncounterCard(face, effect)
                    break
        # « Place X additional threat on Pincer Maneuver, where X is equal to
        # 3 minus the recorded number of evasion counters. » Jamais negatif.
        scheme = ChercherDansLeDeckRencontre(effect, '16112')
        scheme.Reveal(Worlds.GetFirstPlayer(effect), effect)
        surplus = max(0, 3 - _entier(effect, 'Evasion Counters'))
        if surplus:
            scheme.PlaceThreatInternal(surplus, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def EachPlayerMarketCardsIntoDeck() -> 'Ability':
    """Ce qu'on a achete au Marche reste dans le deck pour toute la campagne.

    Livret p.5 : « Cards added to a player's deck this way must be included in
    that player's deck for the rest of the campaign and do not count toward
    that player's minimum or maximum deck size. » Le deck sauvegarde de la
    campagne ne les contient pas — elles vivent au carnet, comme les
    ameliorations de role de Mutant Genesis ou l'allie de campagne d'AoA. On
    les remet donc a chaque mise en place.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            ids = _liste(CampaignLog.GetStrByPlayer('Market Cards', player.player_id, effect))
            for card_id in ids:
                card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                Faces.ShuffleAllTo([card.face], player.player_deck, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


# La Pierre du Pouvoir, l'amelioration d'artefact que le scenario 4 peut laisser
# accrochee a un heros.
#
# CORRECTIF DU 19/09/2026, trouve par les epreuves de campagne : le releve
# cherchait une carte « 16110 », qui est en realite « Fanaticism », une
# condition posee sur Ronan au scenario 5. La Pierre du Pouvoir est 16149, et
# c'est une ATTACHMENT, pas une amelioration — les deux erreurs se cumulaient,
# la case « Power Stone Control » n'etait donc jamais remplie et « Vous etes
# accuse ! » n'arrivait jamais au scenario 5.
PIERRE_DU_POUVOIR = '16149'


def PorteLaPierreDuPouvoir(identity: 'CardFace') -> bool:
    attachees = list(identity.GetAttachedAttachments()) + list(identity.GetAttachedUpgrades())
    return any(f.paper.card_id.startswith(PIERRE_DU_POUVOIR) for f in attachees)


def NomDeHeros(identity: 'CardFace') -> str:
    """Le nom de la face HEROS, quelle que soit la forme active.

    CORRECTIF DU 19/09/2026 : le carnet notait `identity.paper.name`, donc
    « Steve Rogers » si la partie se terminait en alter-ego. A la mise en place
    du scenario suivant, chaque joueur commence en ALTER-EGO : la comparaison
    ne pouvait pas retomber sur ses pieds. On ecrit et on relit desormais le
    nom de heros, seul nom stable d'un bout a l'autre de la campagne.
    """
    try:
        face = identity.GetHeroFace()
    except AssertionError:
        face = None
    return (face or identity).paper.name.lstrip('* ')


def CampaignSetup(level: int) -> 'List[Ability]':
    """Ce que la manigance principale 1A du scenario `level` doit appeler."""
    abilities: List['Ability'] = [RevelerLaManiganceDeCampagne(level),
                                  MelangerLeChasseurEtSesRenforts(),
                                  EachPlayerMarketCardsIntoDeck()]
    if level == 3:
        abilities.append(RetirerLesCartesDeLaCollection())
    if level == 4:
        abilities.append(RemelangerLesArtefacts())
    if level == 5:
        abilities.append(PoserLaSuiteDeRonan())
    if level >= 2:
        # Degats persistants. Le soin coute 1 unite, prelevee au carnet : c'est
        # une depense, elle se fait a l'ecran avant le lancement, le moteur ne
        # sachant pas debiter le carnet en cours de partie.
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect, message: CollectGMW(level, effect),
                                                scenario_id=IDS_SCENARIOS[level - 1]))
    return abilities


# ------------------------------------------------------------------ releve --
def _unites_gagnees(level: int, effect: 'Effect') -> int:
    """Les unites d'une victoire, par joueur. Livret, puce par puce."""
    total = 1                                   # « Record 1 unit for each player. »
    # « a number of units (to a maximum of 3) equal to the victory values on
    # encounter cards in the victory display »
    #
    # CORRECTIF DU 19/09/2026 : on additionnait `face.victory`, qui est un
    # BOOLEEN (« cette carte a-t-elle une valeur de victoire »,
    # has_victory.py:50), pas la valeur. On comptait donc les CARTES et non
    # les points : deux manigances « Victory 0 » rapportaient 2 unites au lieu
    # de 0, et un sbire « Victory 2 » n'en rapportait qu'une. La valeur
    # imprimee est `printed_victory`.
    valeurs = 0
    for face in effect.world.victory_display.Get():
        valeurs += int(getattr(face, 'printed_victory', 0) or 0)
    total += min(3, valeurs)

    if level == 1:
        if not Worlds.FindCardsOnField(effect, card_type=Minion):
            total += 1
        if ActiveMainSchemeStartswith(effect, '16061b'):
            total += 1
    elif level == 2:
        if len(CartesDeLaCollection(effect)) <= 1:
            total += 1
        if all(s.threat == 0 for s in Worlds.GetAllMainSchemes(effect.world)):
            total += 1
    elif level == 3:
        total += len(_artefacts_en_pile_victoire(effect)) // 2
    elif level == 4:
        if CompteursEsquive(effect) <= 1:
            total += 1
        if ActiveMainSchemeStartswith(effect, '16091b'):
            total += 1
    return total


def _artefacts_en_pile_victoire(effect: 'Effect') -> 'List[str]':
    """Les manigances « artefact galactique » posees en pile de victoire.

    Par card_id, pas par trait : voir le commentaire d'ARTEFACTS.
    """
    noms = []
    for face in effect.world.victory_display.Get():
        nom = ARTEFACTS.get(face.paper.card_id)
        if nom:
            noms.append(nom)
    return noms


def CollectGMW(level: int, effect: 'Effect') -> dict:
    """Ce que le moteur sait constater a la fin du scenario `level`."""
    updates: Dict[str, Any] = {}
    gagnees = _unites_gagnees(level, effect)
    for player in Worlds.GetPlayers(effect):
        # Les unites S'ACCUMULENT : « add these to units you already have ».
        avant = _entier(effect, f'Player {(player.player_id + 1)} Unspent Units')
        updates[f'Player {(player.player_id + 1)} Unspent Units'] = str(avant + gagnees)

    if FaceExists(effect, CHASSEUR, in_victory=True):
        updates[f'Headhunter Defeated: {SCENARIOS[level - 1]}'] = '1'

    if level == 2:
        for player in Worlds.GetPlayers(effect):
            ids = [f.paper.card_id for f in CartesDeLaCollection(effect)
                   if f.GetControlByOrOwner() == player]
            if ids:
                updates[f'Player {(player.player_id + 1)} Collection Cards'] = SEPARATEUR.join(ids)

    if level == 3:
        artefacts = _artefacts_en_pile_victoire(effect)
        if artefacts:
            updates['Galactic Artifacts in Victory Display'] = SEPARATEUR.join(artefacts)

    if level == 4:
        updates['Evasion Counters'] = str(CompteursEsquive(effect))
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            if identity and PorteLaPierreDuPouvoir(identity):
                updates['Power Stone Control'] = NomDeHeros(identity)
                break

    return updates
