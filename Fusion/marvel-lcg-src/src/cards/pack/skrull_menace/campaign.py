"""Campagne « Skrull Menace » (Kajislav, livret 1.5) : mise en place, regle de
cooperation et releve du carnet.

Livret : p.5-6 (regles de campagne, Cooperation Progress, campagne experte), p.7
(Shaper of Worlds, ensembles Skrull Elite), p.9, 11, 13, 15, 17 (encarts CAMPAIGN
INSTRUCTIONS des cinq scenarios), p.21 (FAQ), p.22-24 (carnet et tableau
« Cooperation Progress »). Chaque regle, avec sa page, son implementation et le cas
qui la prouve, est dans `.planning/skrull-menace/CAMPAGNE-MODE.md`.

Ce que ce fichier fait, dans l'ordre ou le livret le demande :

  * MISE EN PLACE (`MiseEnPlace`, une seule capacite pour que l'ordre des pas soit
    celui du livret) : sets Standard / Expert alternatifs, Shaper of Worlds et Cosmic
    Cube Creation, ensemble Skrull Elite tire au hasard (plus ceux qu'on traine),
    cartes de la Cooperation Area que chaque joueur melange a son deck, puis la
    campagne EXPERTE (PV restants, soin par pion Acceleration, joueur elimine).
  * REGLE DE COOPERATION (`RegleDeCooperation`) : quand un joueur vainc un sbire ou
    un complot annexe, il peut defausser le dessus de son deck pour le placer dans
    la pile de victoire. Valable pendant toute la partie.
  * RELEVE (`Releve`, a la fin d'une partie GAGNEE) : tableau « Cooperation Progress »,
    cartes ajoutees a la Cooperation Area, zone de jeu du Shaper, de Cosmic Cube
    Creation et de chaque Elite, PV restants.

Cles du carnet (toutes declarees dans `data/campagnes/skrull_menace.json`, car le
panneau de recompenses ne reporte QUE les cles declarees) :

  - `Cooperation Area` : ids des cartes de campagne disponibles (zone commune) ;
  - `Cooperation Progress` : « <carte>: <exigence> » pour chaque case cochee du tableau ;
  - `Shaper of Worlds Game Area`, `Cosmic Cube Creation Game Area` ;
  - `Skrull Elite: <nom>` : zone de jeu de chaque Elite deja tiree ;
  - `Eliminated Players` : sieges elimines a la fin de la partie (campagne experte) ;
  - `Alternative Standard Set`, `Alternative Expert Set` : reglages de la campagne ;
  - `Player N Remaining hit points`, `Player N Identity` (communes a toutes les boites).

Aucune de ces cartes de campagne (sk263-sk288) n'est requise pour que CE module se
charge : il ne les fabrique qu'au moment de s'en servir, et type chaque id par sa
table ci-dessous (repli : le type de la fiche de la carte).
"""
from cards.pack import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver, FaceExists
from itertools import combinations

SEP = ';'

# Les cinq scenarios, dans l'ordre du livret. C'est aussi l'estampille du carnet sortant
# (le panneau de recompenses ignore tout releve dont l'estampille differe de l'id du
# scenario de `data/campagnes/skrull_menace.json`).
SCENARIOS = ['sk_skrull_empire', 'sk_super_skrull', 'sk_paibok', 'sk_skrull_pantheon', 'sk_secret_invasion']

# ------------------------------------------------------------------ les cles --
CLE_ZONE = 'Cooperation Area'
CLE_PROGRES = 'Cooperation Progress'
CLE_SHAPER = 'Shaper of Worlds Game Area'
CLE_CUBE = 'Cosmic Cube Creation Game Area'
CLE_ELIMINES = 'Eliminated Players'
CLE_ALT_STANDARD = 'Alternative Standard Set'
CLE_ALT_EXPERT = 'Alternative Expert Set'


def CleElite(nom: str) -> str:
    return f'Skrull Elite: {nom}'


# Les zones de jeu que le carnet note (livret p.22-23). Libelles = ceux du carnet imprime.
EN_JEU = 'In play'
MIS_DE_COTE = 'Set aside, out of play'
AUTRE_ZONE = 'In another game area'
PILE_VICTOIRE = 'In the victory display'
RETIRE = 'Removed from campaign'

# ----------------------------------------------------------- les cartes -------
SHAPER = 'sk228'          # le sbire Shaper of Worlds
CUBE = 'sk229'            # le complot annexe Cosmic Cube Creation
FRAGMENTS = ['sk230a', 'sk230b', 'sk230c', 'sk230d']   # la ressource Cosmic Cube Fragment, 4 exemplaires

# Les cinq ensembles Skrull Elite : le sbire, l'ensemble, l'allie de campagne portant le
# meme titre, et le complot annexe de joueur de l'aspect de cet allie (p.9 : « the ally
# matching the title of the Skrull Elite minion in the victory display and a player side
# scheme matching the aspect of that ally »).
ELITES = [
    {'nom': 'Crusader',   'ensemble': 'sk_skrull_elite_crusader',   'sbire': 'sk231', 'allie': 'sk263',
     'aspect': 'Aggression', 'complot': 'sk273'},   # Newbie Training
    {'nom': 'Jazinda',    'ensemble': 'sk_skrull_elite_jazinda',    'sbire': 'sk236', 'allie': 'sk264',
     'aspect': 'Justice', 'complot': 'sk276'},      # Stealing for Good
    {'nom': 'Skymax',     'ensemble': 'sk_skrull_elite_skymax',     'sbire': 'sk241', 'allie': 'sk266',
     'aspect': 'Leadership', 'complot': 'sk272'},   # Fickle Alliance
    {'nom': 'War Skrull', 'ensemble': 'sk_skrull_elite_war_skrull', 'sbire': 'sk245', 'allie': 'sk268',
     'aspect': 'Pool', 'complot': 'sk271'},         # Cloning Faux Pas
    {'nom': 'Xavin',      'ensemble': 'sk_skrull_elite_xavin',      'sbire': 'sk250', 'allie': 'sk269',
     'aspect': 'Protection', 'complot': 'sk270'},   # Buddy Training Program
]

# Ce que la VICTOIRE d'un scenario ajoute a la Cooperation Area, hors Elites (p.11 et p.13).
AJOUTS_DE_SCENARIO = {
    2: ['sk267', 'sk274'],   # Super-Skrull (allie) + Searching for Powers
    3: ['sk265', 'sk275'],   # Paibok (allie) + Skrull Military Training
}

# Les cinq types de carte de la zone, dans l'ordre des colonnes du carnet (p.22).
TYPES_DE_LA_ZONE = ['Ally', 'PlayerSideScheme', 'Resource', 'Support', 'Upgrade']

# Le type de chaque carte de campagne (livret : alliés 263-269, complots annexes de joueur
# 270-276, soutiens 277-282, ameliorations 283-288 ; les fragments sont LA ressource).
TYPE_DES_CARTES: Dict[str, str] = {}
for _n in range(263, 270):
    TYPE_DES_CARTES[f'sk{_n}'] = 'Ally'
for _n in range(270, 277):
    TYPE_DES_CARTES[f'sk{_n}'] = 'PlayerSideScheme'
for _n in range(277, 283):
    TYPE_DES_CARTES[f'sk{_n}'] = 'Support'
for _n in range(283, 289):
    TYPE_DES_CARTES[f'sk{_n}'] = 'Upgrade'
for _f in FRAGMENTS:
    TYPE_DES_CARTES[_f] = 'Resource'

# L'ordre canonique de la zone (celui de la planche imprimee), pour un carnet stable.
ORDRE_DE_LA_ZONE = [f'sk{n}' for n in range(263, 289)] + FRAGMENTS

# ---------------------------------------------- le tableau Cooperation Progress --
# Livret p.24, relu ligne a ligne. (carte, titre imprime, [exigences], cartes ajoutees).
# « Skrull Kill Crew » est ecrit ainsi dans le tableau, « Krew » sur la carte : on garde
# la graphie du tableau, qui est ce que le joueur lit dans son carnet.
PROGRESSION = [
    ('sk277', 'Antalya', ['Nemesis minion', 'Seeking a Suitable World'], ['sk277']),
    ('sk278', 'Cadre K', ['Non-ELITE minion', 'Hijacked', 'GENIUS minion'], ['sk278']),
    ('sk279', 'Pool-o-Vision', ['ELITE non-SKRULL minion', 'ELITE SKRULL minion', 'Non-ELITE SKRULL minion'], ['sk279']),
    ('sk280', 'Princess Anelle', ['Cloning Program', "Emperor's Throne"], ['sk280']),
    ('sk281', 'Skrull Battleship', ['SOLDIER minion', 'Hijacked', 'Seeking a Suitable World'], ['sk281']),
    ('sk282', 'Skrull Kill Crew', ['Skrull Spy', 'Skrull Warrior', 'Skrull Soldier', 'Skrull Commander'], ['sk282']),
    ('sk283', "3-D Man's Goggles", ['ELITE minion', 'Non-SKRULL minion', 'Player side scheme', 'Non-unique minion'], ['sk283']),
    ('sk284', 'Inhibitor Mask', ['Plotting Revenge', 'Non-ELITE non-SKRULL minion'], ['sk284']),
    ('sk285', 'Nullifier', ['Nemesis side scheme'], ['sk285']),
    ('sk286', 'Reverting Device', ['Skrull Spy', 'Skrull Scientist', 'Skrull Warrior', 'Skrull Telepath'], ['sk286']),
    ('sk287', 'Skrull Shapeshifter', ['Unique minion', 'Plotting Revenge', 'SKRULL minion'], ['sk287']),
    ('sk288', 'Sy-Torak Gem', ['Jazinda', 'Stealing for the Empire'], ['sk288']),
    # Resources : la FAQ (p.21) dit « all copies of the Cosmic Cube Fragment ».
    ('sk230', 'Cosmic Cube Fragment', ['Cosmic Cube Creation'], list(FRAGMENTS)),
]

# Les exigences qui nomment une CARTE (un titre) et non une categorie : (type, titre).
TITRES = {
    'Seeking a Suitable World': ('SideScheme', 'Seeking a Suitable World'),
    'Hijacked': ('SideScheme', 'Hijacked'),
    'Cloning Program': ('SideScheme', 'Cloning Program'),
    "Emperor's Throne": ('SideScheme', "Emperor's Throne"),
    'Plotting Revenge': ('SideScheme', 'Plotting Revenge'),
    'Stealing for the Empire': ('SideScheme', 'Stealing for the Empire'),
    'Cosmic Cube Creation': ('SideScheme', 'Cosmic Cube Creation'),
    'Skrull Spy': ('Minion', 'Skrull Spy'),
    'Skrull Warrior': ('Minion', 'Skrull Warrior'),
    'Skrull Soldier': ('Minion', 'Skrull Soldier'),
    'Skrull Commander': ('Minion', 'Skrull Commander'),
    'Skrull Scientist': ('Minion', 'Skrull Scientist'),
    'Skrull Telepath': ('Minion', 'Skrull Telepath'),
    'Jazinda': ('Minion', 'Jazinda'),
}


def RangDeRarete(exigence: str) -> int:
    """0 : un titre precis ; 1 : une categorie etroite (nemesis, joueur, trait propre a quelques
    cartes) ; 2 : un « Non-... » ou une categorie large (ELITE, SKRULL, unique)."""
    if exigence in TITRES:
        return 0
    if exigence in ('Nemesis minion', 'Nemesis side scheme', 'Player side scheme',
                    'GENIUS minion', 'SOLDIER minion', 'ELITE non-SKRULL minion'):
        return 1
    return 2


def CarteDuTableau(nom: str, type_: str, traits: 'Sequence[str]', unique: bool, nemesis: bool, joueur: bool) -> dict:
    """Ce que le tableau sait lire d'une carte de la pile de victoire."""
    return {'nom': nom, 'type': type_, 'traits': {t.upper() for t in traits}, 'unique': unique,
            'nemesis': nemesis, 'joueur': joueur}


def ExigenceRemplie(exigence: str, carte: dict) -> bool:
    """Cette carte peut-elle cocher cette exigence du tableau ? (p.24)

    « minion » = un sbire ; « side scheme » = un complot annexe (de rencontre, de nemesis
    ou de joueur) ; un mot en capitales = un trait ; « Non- » devant lui le nie.
    """
    if exigence in TITRES:
        type_, titre = TITRES[exigence]
        return carte['type'] == type_ and carte['nom'] == titre
    traits = carte['traits']
    sbire = carte['type'] == 'Minion'
    if exigence == 'Nemesis minion':
        return sbire and carte['nemesis']
    if exigence == 'Nemesis side scheme':
        return carte['type'] == 'SideScheme' and carte['nemesis']
    if exigence == 'Player side scheme':
        return carte['type'] == 'SideScheme' and carte['joueur']
    if not sbire:
        return False
    if exigence == 'Unique minion':
        return carte['unique']
    if exigence == 'Non-unique minion':
        return not carte['unique']
    elite = 'ELITE' in traits
    skrull = 'SKRULL' in traits
    return {
        'Non-ELITE minion': not elite,
        'ELITE minion': elite,
        'GENIUS minion': 'GENIUS' in traits,
        'SOLDIER minion': 'SOLDIER' in traits,
        'SKRULL minion': skrull,
        'Non-SKRULL minion': not skrull,
        'ELITE non-SKRULL minion': elite and not skrull,
        'ELITE SKRULL minion': elite and skrull,
        'Non-ELITE SKRULL minion': skrull and not elite,
        'Non-ELITE non-SKRULL minion': not elite and not skrull,
    }.get(exigence, False)


def _jumelage(cartes: List[dict], exigences: List[Tuple[str, str]]) -> 'Dict[int, int]|None':
    """Une carte DISTINCTE par exigence (« each card in the victory display can be used to
    check off only one requirement », p.6). Chemins augmentants ; rend {exigence: carte} ou
    None si une exigence reste sans carte."""
    pris: Dict[int, int] = {}      # carte -> exigence

    def placer(i: int, vues: set) -> bool:
        for c, carte in enumerate(cartes):
            if c in vues or not ExigenceRemplie(exigences[i][1], carte):
                continue
            vues.add(c)
            if c not in pris or placer(pris[c], vues):
                pris[c] = i
                return True
        return False

    for i in range(len(exigences)):
        if not placer(i, set()):
            return None
    return {e: c for c, e in pris.items()}


def AssignerLaProgression(cartes: List[dict], cochees: 'Set[Tuple[str, str]]') -> 'Tuple[Set[Tuple[str, str]], List[str]]':
    """Coche le tableau avec les cartes de la pile de victoire.

    Rend (cases nouvellement cochees, titres des lignes qui deviennent completes).

    Le livret laisse le joueur choisir quelle carte coche quelle case. Le moteur prend la
    reponse qui sert le plus : d'abord le plus grand nombre de LIGNES completes (une ligne
    complete = une carte de campagne gagnee, donc ce qui compte), puis, avec les cartes qui
    restent, le plus de cases cochees (rien ne se perd : le progres est garde pour plus tard).
    A egalite, l'ordre du tableau imprime tranche.
    """
    ouvertes = []
    for _, titre, exigences, _ in PROGRESSION:
        restantes = [(titre, e) for e in exigences if (titre, e) not in cochees]
        ouvertes.append((titre, restantes))

    # Les lignes deja pleines (cochees a la main au carnet) n'ont pas besoin de cartes.
    deja_pleines = [titre for titre, restantes in ouvertes if not restantes]
    a_remplir = [(titre, restantes) for titre, restantes in ouvertes if restantes]

    meilleur: 'Tuple[List[str], Dict[Tuple[str, str], int]]|None' = None
    for taille in range(len(a_remplir), -1, -1):
        for choix in combinations(range(len(a_remplir)), taille):
            exigences = [x for i in choix for x in a_remplir[i][1]]
            if len(exigences) > len(cartes):
                continue
            jumelage = _jumelage(cartes, exigences)
            if jumelage is None:
                continue
            meilleur = ([a_remplir[i][0] for i in choix],
                        {exigences[e]: c for e, c in jumelage.items()})
            break
        if meilleur is not None:
            break
    assert meilleur is not None            # taille 0 : toujours jumelable (rien a placer)
    completes, jumeles = meilleur
    nouvelles: Set[Tuple[str, str]] = set(jumeles)

    # Les cartes qui restent cochent ce qu'elles peuvent des lignes non completees.
    libres = [c for c in range(len(cartes)) if c not in set(jumeles.values())]
    autres = [x for titre, restantes in a_remplir if titre not in completes for x in restantes]
    # Une carte de la pile ne coche QU'UNE case : on la met sur la plus RARE (un titre, avant une
    # categorie large), pour garder les exigences faciles pour plus tard. Tri stable : a rang egal,
    # l'ordre du tableau imprime.
    autres.sort(key=lambda x: RangDeRarete(x[1]))
    # Plus grand jumelage partiel : on essaie d'ajouter les exigences une a une (glouton
    # avec reprise par chemins augmentants, comme `_jumelage`).
    sous_cartes = [cartes[c] for c in libres]
    retenues: List[Tuple[str, str]] = []
    for x in autres:
        if _jumelage(sous_cartes, retenues + [x]) is not None:
            retenues.append(x)
    nouvelles |= set(retenues)

    toutes = set(cochees) | nouvelles
    devenues_completes = [titre for _, titre, exigences, _ in PROGRESSION
                          if all((titre, e) in toutes for e in exigences)
                          and not all((titre, e) in cochees for e in exigences)]
    # Les lignes pleines AVANT la partie sont aussi a verser a la zone (carnet corrige a la main).
    for titre in deja_pleines:
        if titre not in devenues_completes:
            devenues_completes.append(titre)
    return nouvelles, devenues_completes


def ParseProgres(valeur: List[str]) -> 'Set[Tuple[str, str]]':
    sortie = set()
    for item in valeur:
        if ': ' in item:
            titre, exigence = item.split(': ', 1)
            sortie.add((titre, exigence))
    return sortie


def FormatProgres(cochees: 'Set[Tuple[str, str]]') -> str:
    """Dans l'ordre du tableau imprime, une case par « <carte>: <exigence> »."""
    ordre = []
    for _, titre, exigences, _ in PROGRESSION:
        for e in exigences:
            if (titre, e) in cochees:
                ordre.append(f'{titre}: {e}')
    return SEP.join(ordre)


def CartesAjouteesParLigne(titres: List[str]) -> List[str]:
    ids: List[str] = []
    for _, titre, _, ajouts in PROGRESSION:
        if titre in titres:
            ids += ajouts
    return ids


def OrdonnerLaZone(ids: 'Sequence[str]') -> List[str]:
    """Sans doublon, dans l'ordre imprime ; un id inconnu va a la fin, dans l'ordre d'arrivee."""
    uniques = list(dict.fromkeys(ids))
    connus = [i for i in ORDRE_DE_LA_ZONE if i in uniques]
    return connus + [i for i in uniques if i not in connus]


# ---------------------------------------------------------------- lectures --
def _liste(effect: 'Effect', cle: str) -> List[str]:
    return CampaignLog.GetListInternal(cle, effect)


def _texte(effect: 'Effect', cle: str) -> str:
    return CampaignLog.GetStrInternal(cle, effect)


def TypeDeLaCarte(card_id: str) -> str:
    """Le type d'une carte de la zone : la table du livret, puis la fiche de la carte."""
    if card_id in TYPE_DES_CARTES:
        return TYPE_DES_CARTES[card_id]
    from cards.database import CardsDB
    paper = CardsDB.papers.get(card_id)
    return paper.type if paper else ''


def NomDeLaCarte(card_id: str) -> str:
    from cards.database import CardsDB
    paper = CardsDB.papers.get(card_id)
    return paper.name if paper else card_id


def _elites_jamais_tirees(effect: 'Effect') -> List[dict]:
    return [e for e in ELITES if not _texte(effect, CleElite(e['nom']))]


def _generer(effect: 'Effect', card_id: str) -> 'CardFace':
    return CardFactory.GenerateCard(card_id, None, effect.world).face


def _mettre_de_cote(effect: 'Effect', card_id: str) -> 'CardFace':
    """Une carte creee directement dans la zone « mise de cote » du scenario."""
    return CardFactory.GenerateCard(card_id, effect.world.aside_deck, effect.world).face


# ------------------------------------------------------------ mise en place --
def _sets_alternatifs(effect: 'Effect') -> None:
    """Standard Skrull / Expert Skrull remplacent Standard / Expert (p.4, « Alternative Sets »)."""
    echanges = [(CLE_ALT_STANDARD, 'standard', 'standard_skrull')]
    if Worlds.IsExpert(effect):
        echanges.append((CLE_ALT_EXPERT, 'expert', 'expert_skrull'))
    for cle, ancien, nouveau in echanges:
        if _texte(effect, cle) != '1':
            continue
        restants = list(Worlds.GetEncounterDeckCards(effect))
        a_retirer = []
        for card_id in CardFactory.LoadEncounterSet(ancien):
            for face in restants:
                if face.paper.card_id == card_id:
                    a_retirer.append(face)
                    restants.remove(face)
                    break
        if a_retirer:
            Faces.RemoveAllFromGame(a_retirer, effect)
        faces = [_generer(effect, i) for i in CardFactory.LoadEncounterSet(nouveau)]
        Faces.ShuffleAllTo(faces, 'EncounterDeck', effect)


def _shaper_et_cube(effect: 'Effect', level: int) -> None:
    """Shaper of Worlds et Cosmic Cube Creation (p.7, p.9 pour le scenario 1, p.10 pour les
    suivants). Aucun carnet (scenario 1, ou jeu lance sans carnet) : le complot est melange au
    deck rencontre, le sbire et un fragment par joueur sont mis de cote."""
    joueurs = list(Worlds.GetPlayers(effect))
    premier = Worlds.GetFirstPlayer(effect)
    shaper = _texte(effect, CLE_SHAPER)
    cube = _texte(effect, CLE_CUBE)

    # --- Shaper of Worlds
    if shaper == EN_JEU:
        face = _generer(effect, SHAPER)
        face.PutIntoPlay(premier, effect)
    elif shaper == AUTRE_ZONE:
        Faces.ShuffleAllTo([_generer(effect, SHAPER)], 'EncounterDeck', effect)
    else:                                       # « Set aside » ou jamais note
        _mettre_de_cote(effect, SHAPER)

    # --- Cosmic Cube Creation et ses fragments
    if cube == '' or cube == AUTRE_ZONE:        # scenario 1 : « Shuffle ... into the encounter deck »
        Faces.ShuffleAllTo([_generer(effect, CUBE)], 'EncounterDeck', effect)
    elif cube == EN_JEU:
        _generer(effect, CUBE).PutIntoPlay(premier, effect)
    elif cube == PILE_VICTOIRE:                 # « remove it from the campaign »
        CampaignLog.SetStr(CLE_CUBE, RETIRE, effect.world)
    if cube in ('', AUTRE_ZONE, EN_JEU):        # un fragment par joueur, mis de cote
        nombre = min(len(joueurs), len(FRAGMENTS))
        copies = list(FRAGMENTS) if nombre >= len(FRAGMENTS) else Rand.RandomChoice2(list(FRAGMENTS), nombre, effect)
        for card_id in copies:
            _mettre_de_cote(effect, card_id)


def _elites(effect: 'Effect', level: int) -> None:
    """Les ensembles Skrull Elite (p.9 a p.17).

    * une Elite deja tiree dont le sbire etait en pile de victoire quitte la campagne ;
    * une Elite deja tiree dont le sbire etait ailleurs est remelangee avec son ensemble ;
    * une Elite jamais tiree : UNE au hasard aux scenarios 1 a 4 (« one other random »),
      TOUTES celles qui restent au scenario 5 (« the remaining » : exactement une dans une
      campagne jouee en entier).
    """
    pioche: List[dict] = []
    for elite in ELITES:
        etat = _texte(effect, CleElite(elite['nom']))
        if etat == PILE_VICTOIRE:
            CampaignLog.SetStr(CleElite(elite['nom']), RETIRE, effect.world)
        elif etat == AUTRE_ZONE:
            pioche.append(elite)
    candidates = _elites_jamais_tirees(effect)
    if level >= 5:
        pioche += candidates
    elif candidates:
        pioche.append(candidates[Rand.RandomChoice(list(range(len(candidates))), effect)])
    for elite in pioche:
        faces = [_generer(effect, i) for i in CardFactory.LoadEncounterSet(elite['ensemble'])]
        Faces.ShuffleAllTo(faces, 'EncounterDeck', effect)


def _cartes_de_la_zone(effect: 'Effect') -> None:
    """Scenarios 2 a 5 : chaque joueur peut melanger une carte de chaque type de la
    Cooperation Area a son deck (p.5, p.10). Ces cartes sont hors limite du deck (generees APRES
    la composition du deck) et rendues a la zone apres la partie (le carnet ne les en retire
    jamais)."""
    zone = list(_liste(effect, CLE_ZONE))
    for player in Worlds.GetPlayers(effect):
        if player.is_eliminated:
            continue
        ajoutees = False
        for type_ in TYPES_DE_LA_ZONE:
            candidates = [i for i in zone if TypeDeLaCarte(i) == type_]
            if not candidates:
                continue
            noms = [NomDeLaCarte(i) for i in candidates]
            choisie = player.AskChooseOneText(candidates + [None], noms + ['Cancel'],
                                              titre=f'Cooperation Area: add a card ({type_})')
            if choisie:
                zone.remove(choisie)             # une carte unique ne va que dans UN deck
                CardFactory.GenerateCard(choisie, player.player_deck, effect.world)
                ajoutees = True
        if ajoutees:
            player.player_deck.Shuffle(effect)


def _campagne_experte(effect: 'Effect') -> None:
    """p.6 : PV persistants, soin par pion Acceleration, joueur elimine qui revient."""
    this = effect.this
    elimines = _liste(effect, CLE_ELIMINES)
    for player in Worlds.GetPlayers(effect):
        identity = player.GetIdentity()
        siege = str(player.player_id + 1)
        revient = siege in elimines
        restants = CampaignLog.GetIntByPlayer('Remaining hit points', player.player_id, effect)
        if not revient and restants > 0:
            identity.SetHealth(min(restants, identity.max_health), effect)
        if not revient and identity.health >= identity.max_health:
            continue

        def soigner(targets: Sequence['CardFace'], this=this, identity=identity) -> None:
            this.PlaceTokensInternal(1, 'acceleration_token', effect)
            identity.CastTo(CanHealth).HealHealth('All', effect)
        libelle = ('Place 1 acceleration token on the main scheme to rejoin the team at full hit points'
                   if revient else 'Place 1 acceleration token on the main scheme to heal to full')
        pris = player.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility(libelle, soigner))
        if revient and pris is None:
            player.Eliminate(effect)             # il ne revient pas : il ne joue pas ce scenario


def MiseEnPlace(level: int) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        _sets_alternatifs(effect)
        _shaper_et_cube(effect, level)
        _elites(effect, level)
        if level >= 2:
            _cartes_de_la_zone(effect)
            if Worlds.IsExpert(effect):
                _campagne_experte(effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


# ----------------------------------------------------- la regle de cooperation --
def _peut_cooperer(face: 'CardFace', joueur: 'Player|None') -> bool:
    if joueur is None or joueur.is_eliminated:
        return False
    if face.victory:                              # Victory X : elle y va deja, sans rien defausser
        return False
    if face.HasTrait('REVEALED'):                 # FAQ p.21 : un sbire Revealed va a la defausse Impostor
        return False
    return joueur.player_deck.GetSize() > 0


def _proposer(effect: 'Effect', face: 'CardFace', joueur: 'Player') -> None:
    def placer(targets: Sequence['CardFace']) -> None:
        Faces.DiscardAll(joueur.player_deck.GetTops(1), effect)
        Faces.AddToVictoryDisplay([face], effect)
    joueur.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility(
        f'Discard the top card of your deck to place {face.name} in the victory display', placer))


def RegleDeCooperation() -> List['Ability']:
    """p.6 et carte « Cooperation Progress Reminder » : « When a player defeats a minion or a
    side scheme, that player may discard the top card of their deck to place that minion or side
    scheme in the victory display instead of the encounter discard pile. »"""
    def sbire(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        face = message.trigger
        if Minion.IsType(face) and _peut_cooperer(face, message.defeating_player):
            _proposer(effect, face, message.defeating_player)

    def complot(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        face = message.trigger
        if SchemeSide2.IsType(face) and not MainScheme.IsType(face) \
                and _peut_cooperer(face, message.defeating_player):
            _proposer(effect, face, message.defeating_player)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.Campaign, Minion, sbire,
                                          has_defeating_player=True,
                                          conditions=[lambda e, m: Worlds.IsCampaign(e)]),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.Campaign, SchemeSide2, complot,
                                            has_defeating_player=True,
                                            conditions=[lambda e, m: Worlds.IsCampaign(e)]),
    ]


# -------------------------------------------------------------------- releve --
def _carte_du_tableau(face: 'CardFace') -> dict:
    paper = face.paper
    return CarteDuTableau(paper.name, 'Minion' if Minion.IsType(face) else 'SideScheme', paper.traits,
                          bool(paper.is_unique), str(paper.set_name).endswith(' Nemesis'),
                          PlayerSideScheme.IsType(face))


def _zone_de_jeu(effect: 'Effect', card_id: str, etat_avant: str) -> str:
    """La zone de jeu d'une carte a la fin de la partie, au vocabulaire du carnet."""
    if etat_avant == RETIRE:
        return RETIRE
    if not FaceExists(effect, card_id):
        return etat_avant
    if FaceExists(effect, card_id, in_victory=True):
        return PILE_VICTOIRE
    if FaceExists(effect, card_id, in_play=True):
        return EN_JEU
    if any(f.paper.card_id == card_id for f in Worlds.GetSetAsideAreaCards(effect)):
        return MIS_DE_COTE
    return AUTRE_ZONE


def Releve(level: int, effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """Ce que le livret fait noter a la VICTOIRE du scenario `level` (rien a la defaite : on
    rejoue sans penalite). Le scenario 5 n'a qu'une ligne : Veranke vaincue, campagne gagnee."""
    if not message.players_won:
        return {}
    updates: Dict[str, Any] = {}
    world = effect.world

    # --- Campagne experte : PV restants (plafonnes aux PV de base) et joueurs elimines
    elimines = []
    for player in Worlds.GetPlayers(effect):
        identity = player.GetIdentity()
        cle = f'Player {player.player_id + 1} Remaining hit points'
        if player.is_eliminated:
            elimines.append(str(player.player_id + 1))
            updates[cle] = '0'
        elif identity:
            updates[cle] = str(max(0, min(identity.health, identity.printed_health)))
    # Une cle absente du releve laisserait l'ANCIENNE valeur au carnet (le panneau ne sait pas
    # distinguer « effacee » de « jamais ecrite ») : on ecrit une chaine vide, jamais None.
    updates[CLE_ELIMINES] = SEP.join(elimines)

    if level >= 5:
        return updates

    # --- Cooperation Progress (scenarios 1 a 4)
    cartes = [_carte_du_tableau(f) for f in world.victory_display.Get()
              if (Minion.IsType(f) or SchemeSide2.IsType(f)) and not MainScheme.IsType(f)]
    cochees = ParseProgres(_liste(effect, CLE_PROGRES))
    nouvelles, completes = AssignerLaProgression(cartes, cochees)
    updates[CLE_PROGRES] = FormatProgres(cochees | nouvelles)

    zone = list(_liste(effect, CLE_ZONE))
    zone += CartesAjouteesParLigne(completes)
    zone += AJOUTS_DE_SCENARIO.get(level, [])

    # --- Elites : etat de chacune, et allie + complot de joueur si le sbire est en pile de victoire
    for elite in ELITES:
        cle = CleElite(elite['nom'])
        if not FaceExists(effect, elite['sbire']):
            continue                                # pas dans cette partie : rien a noter
        if FaceExists(effect, elite['sbire'], in_victory=True):
            updates[cle] = PILE_VICTOIRE
            zone += [elite['allie'], elite['complot']]
        else:
            updates[cle] = AUTRE_ZONE

    # --- Shaper of Worlds et Cosmic Cube Creation
    updates[CLE_SHAPER] = _zone_de_jeu(effect, SHAPER, _texte(effect, CLE_SHAPER)) or MIS_DE_COTE
    updates[CLE_CUBE] = _zone_de_jeu(effect, CUBE, _texte(effect, CLE_CUBE)) or AUTRE_ZONE

    updates[CLE_ZONE] = SEP.join(OrdonnerLaZone(zone))
    return updates


def CampaignSetup(level: int) -> 'List[Ability]':
    """Ce que la manigance principale 1A du scenario `level` (1 a 5) doit appeler."""
    return [
        MiseEnPlace(level),
        *RegleDeCooperation(),
        WriteCampaignLogAtGameOver(lambda effect, message: Releve(level, effect, message),
                                   scenario_id=SCENARIOS[level - 1]),
    ]
