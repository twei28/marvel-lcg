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
ARTEFACTS = ('Hujadarian Monarch Egg', 'Magical Teapot', "Philosopher's Stone", 'Crystal Ball')

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

    Livret p.14. Les manigances elles-memes reviennent avec le set ; ce sont
    leurs quatre consequences qui se posent ici.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        gardes = _liste(CampaignLog.GetStrInternal('Galactic Artifacts in Victory Display', effect))
        villains = Worlds.GetAllVillains(effect.world)
        for nom in gardes:
            if nom == 'Hujadarian Monarch Egg':
                for env in Worlds.FindCardsOnField(effect, card_type=Environment):
                    env.PlaceCountersInternal(1, 'evasion', effect)
            elif nom == 'Magical Teapot':
                Worlds.GetFirstPlayer(effect).DealEncounterCards(1, effect)
            elif nom == "Philosopher's Stone":
                encounter_deck = Worlds.GetEncounterDeck(effect)
                for villain in villains:
                    top = encounter_deck.GetTop()
                    if top:
                        villain.GiveBoostCard(top, effect)
                    break
            elif nom == 'Crystal Ball':
                if villains:
                    Faces.GiveStatus([villains[0]], 'Tough', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def PoserLaSuiteDeRonan() -> 'Ability':
    """Scenario 5 : la Pierre du Pouvoir se paie, et l'esquive aussi (p.18)."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        porteur = CampaignLog.GetStrInternal('Power Stone Control', effect)
        if porteur:
            for player in Worlds.GetPlayers(effect):
                identity = player.GetIdentity()
                if identity and (identity.paper.name == porteur):
                    card = CardFactory.GenerateCard('16116', None, effect.world)
                    player.DealEncounterCard(card.face, effect)
                    break
        # « Place X additional threat on Pincer Maneuver, where X is equal to
        # 3 minus the recorded number of evasion counters. » Jamais negatif.
        card = CardFactory.GenerateCard('16112', None, effect.world)
        scheme = card.face
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
    abilities.append(WriteCampaignLogAtGameOver(lambda effect: CollectGMW(level, effect)))
    return abilities


# ------------------------------------------------------------------ releve --
def _unites_gagnees(level: int, effect: 'Effect') -> int:
    """Les unites d'une victoire, par joueur. Livret, puce par puce."""
    total = 1                                   # « Record 1 unit for each player. »
    # « a number of units (to a maximum of 3) equal to the victory values on
    # encounter cards in the victory display »
    valeurs = 0
    for face in effect.world.victory_display.Get():
        valeurs += int(getattr(face, 'victory', 0) or 0)
    total += min(3, valeurs)

    if level == 1:
        if not Worlds.FindCardsOnField(effect, card_type=Minion):
            total += 1
        if ActiveMainSchemeStartswith(effect, '16061b'):
            total += 1
    elif level == 2:
        if len(CartesDeLaCollection(effect)) <= 1:
            total += 1
        if all(s.GetThreatInternal() == 0 for s in Worlds.GetAllMainSchemes(effect.world)):
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
    noms = []
    for face in effect.world.victory_display.Get():
        traits = [t.upper() for t in (face.paper.traits or [])]
        if 'GALACTIC ARTIFACT' in traits:
            noms.append(face.paper.name)
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
            if identity and any(u.paper.card_id.startswith('16110')
                                for u in identity.GetAttachedUpgrades()):
                updates['Power Stone Control'] = identity.paper.name
                break

    return updates
