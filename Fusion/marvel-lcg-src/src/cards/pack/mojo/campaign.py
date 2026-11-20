"""Campagne « MojoMania » (pack 39) : mise en place et releve du carnet.

Regles du livret officiel : pages 4-5 (mode campagne, campagne experte), puis
les encarts CAMPAIGN INSTRUCTIONS des pages 9 (MaGog), 13-14 (Spiral), 17 (Mojo).

Tout ici n'agit qu'en mode campagne (`AbilityFactoryCampaign` garde sur
`Worlds.IsCampaign`) : hors campagne rien ne change.

Cles du carnet (contrat avec l'interface, ne pas renommer) :
  « Player N Support / Upgrade #1 » (scenario 1) et « #2 » (scenario 2) : un card_id ;
  « Longshot In Play: Scenario 1 » / « ... 2 » : « 1 » si Longshot (39071) est en jeu a la fin ;
  « Modular Sets Used » : liste « a;b;c » cumulee ; l'interface injecte « Modular Sets This Scenario ».
"""
from . import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver, FaceExists

LONGSHOT = '39071'


def ShuffleLongshotIntoEncounterDeck() -> 'Ability':
    # Scenario 1 : « Shuffle the Longshot ally into the encounter deck. »
    return AbilityFactoryCampaign.ShuffleCardIntoDeck(LONGSHOT, 'EncounterDeck')


def LongshotRevealOrShuffle(level: int) -> 'Ability':
    # Scenarios 2-3 : « If the Longshot ally was in play at the end of the last scenario, one player may reveal him.
    # Otherwise, shuffle him into the encounter deck. »
    # Au scenario 3 « la derniere partie » est le scenario 2 ; au scenario 2, le scenario 1.
    key = f'Longshot In Play: Scenario {level - 1}'
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(LONGSHOT, None, effect.world)
        face = card.face
        if (CampaignLog.GetStrInternal(key, effect) == ''):
            Faces.ShuffleAllTo([face], 'EncounterDeck', effect)
            return
        player = Worlds.GetFirstPlayer(effect)
        def reveal(targets: Sequence['CardFace']):
            # Declenche le « When Revealed » imprime de 39071 (mise en jeu sous controle + surge, non annulable).
            face.Reveal(player, effect)
        def decline(targets: Sequence['CardFace']):
            # Choix retenu (le livret ne dit rien) : un joueur qui ne le revele pas ne le perd pas, il est melange au deck Rencontre.
            Faces.ShuffleAllTo([face], 'EncounterDeck', effect)
        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility('Reveal Longshot', reveal),
            AbilityFactory.ForChoiceAbility('Shuffle Longshot into the encounter deck', decline),
        )
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def _FindCopy(effect: 'Effect', player: 'Player', card_id: str) -> 'CardFace|None':
    # « from any player's deck » : on cherche d'abord dans le deck du joueur, puis dans celui des autres.
    players = [player] + [p for p in Worlds.GetPlayers(effect) if p != player]
    for p in players:
        for face in p.player_deck.Get(True):
            if face.paper.card_id == card_id:
                return face
    return None


def EachPlayerMayPutRecordedCardsIntoPlay(keys: Sequence[str]) -> 'Ability':
    # « Each player may take one copy of [each card] recorded in the campaign log from any player's deck and put it into play
    # under their control. Then, add threat to the main scheme equal to the total cost of the cards put into play this way. »
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        total = [0]
        for player in Worlds.GetPlayers(effect):
            for key in keys:
                card_id = CampaignLog.GetStrByPlayer(key, player.player_id, effect)
                if not card_id:
                    continue
                face = _FindCopy(effect, player, card_id)
                if face is None:
                    continue
                def take(targets: Sequence['CardFace'], face=face, player=player):
                    cost = FacesCounter.GetPrintedCost([face])
                    face.PutIntoPlay(player, effect, under_control=True)
                    if face.IsInPlay():
                        total[0] += cost
                player.MayChooseOneAbility(
                    effect,
                    AbilityFactory.ForChoiceAbility(f'Put {face.paper.name} into play under your control', take),
                )
        if total[0] > 0:
            schemes = Worlds.GetAllMainSchemes(effect)
            if schemes:
                schemes[0].PlaceThreatInternal(total[0], effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


CHAMPION_BOOING_CROWD = '39003a'


def EligibleSupportsAndUpgrades(level: int, effect: 'Effect') -> dict:
    # « Each player may choose one support or upgrade they control with a cost of two or less (three or less if ...) » :
    #  - scenario 1 (p.9) : trois si l'environnement The Champion est du cote BOOING CROWD (face 39003a) ;
    #  - scenario 2 (p.14) : trois s'il y a MOINS DE DIX menaces par joueur sur la manigance principale.
    # Une carte sans cout imprime (« - ») ne peut jamais etre choisie. Rend {player_id: [card_id, ...]} : ce que l'ecran
    # propose, calcule ICI parce que le moteur seul connait le cout IMPRIME (le descripteur de monde ne distingue pas
    # « cout 0 » de « pas de cout »).
    world = effect.world
    players = Worlds.GetPlayers(effect)
    if level == 1:
        limit = 3 if FaceExists(effect, CHAMPION_BOOING_CROWD, in_play=True) else 2
    else:
        threat = sum(int(getattr(s, 'threat', 0) or 0) for s in Worlds.GetAllMainSchemes(world))
        limit = 3 if threat < 10 * max(1, len(players)) else 2
    eligible: dict = {}
    for card in world.object_manager.card_dict.values():
        face = card.face
        if face is None or not face.IsInPlay():
            continue
        if not (Support.IsType(face) or Upgrade.IsType(face)):
            continue
        if not getattr(face, 'has_printed_cost', False):
            continue
        if face.printed_cost.val > limit:
            continue
        controller = card.GetController()
        player_id = getattr(controller, 'player_id', None)
        if player_id is None:
            continue
        ids = eligible.setdefault(player_id, [])
        if face.paper.card_id not in ids:
            ids.append(face.paper.card_id)
    return eligible


def CollectMojo(level: int, effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    updates = {}
    if level in (1, 2):
        # Les cartes que l'ecran de victoire PROPOSE a chaque joueur (cle de travail, jamais lue par le moteur).
        for player_id, ids in EligibleSupportsAndUpgrades(level, effect).items():
            updates[f'Player {player_id + 1} Eligible Support / Upgrade'] = ';'.join(ids)
        if FaceExists(effect, LONGSHOT, in_play=True):
            updates[f'Longshot In Play: Scenario {level}'] = '1'
        # « Check off the name of the modular encounter set used in this scenario » : liste cumulee, sans doublon.
        used = [x for x in CampaignLog.GetStrInternal('Modular Sets Used', effect).split(';') if x]
        for name in CampaignLog.GetStrInternal('Modular Sets This Scenario', effect).split(';'):
            if name and name not in used:
                used.append(name)
        if used:
            updates['Modular Sets Used'] = ';'.join(used)
    return updates


def CampaignSetup(level: int) -> List['Ability']:
    abilities: List['Ability'] = []
    if level == 1:
        abilities.append(ShuffleLongshotIntoEncounterDeck())
    if level >= 2:
        abilities.append(LongshotRevealOrShuffle(level))
        keys = ['Support / Upgrade #1'] if level == 2 else ['Support / Upgrade #1', 'Support / Upgrade #2']
        abilities.append(EachPlayerMayPutRecordedCardsIntoPlay(keys))
        # Expert seulement : PV restants du carnet, puis 1 carte Rencontre face cachee pour se soigner completement.
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(AbilityFactoryCampaign.ExpertCampaignEachPlayerMayDealFacedownEncounterCardYpHealHP(1))
    scenario_id = {1: 'magog', 2: 'spiral', 3: 'mojo'}[level]
    abilities.append(WriteCampaignLogAtGameOver(lambda effect, message: CollectMojo(level, effect, message), scenario_id))
    return abilities
