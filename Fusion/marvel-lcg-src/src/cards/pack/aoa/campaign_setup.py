from . import *
from cards.pack.mts.campaign import InPool, LogSet, EachPlayerShufflesCopyIfPool, ShuffleIntoEncounterIfPool, WriteCampaignLogAtGameOver, FaceExists
from engine.lib import Random
MISSIONS = [
    ('Liberate the Seattle Core', '45166a'),
    ('Evacuate Survivors', '45167a'),
    ('Sabotage the Sea Wall', '45168a'),
    ('Find Lost Mutants', '45169a'),
]
OVERSEERS = [
    ('Mister Sinister', '45179a,45179b'),
    ('The Shadow King', '45180a,45180b'),
    ('Abyss', '45181a,45181b'),
    ('Sugar Man', '45182a,45182b'),
    ('Mikhail Rasputin', '45183a,45183b'),
]
def ShuffleApocalypseModularIntoEncounterDeck() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        encounters = CardFactory.LoadEncounterSet('age_of_apocalypse_WIP')
        encounter_deck = Worlds.GetEncounterDeck(effect)
        CardFactory.GenerateCards(encounters, encounter_deck, effect.world)
        encounter_deck.Shuffle(effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def SetupMissionAndOverseer(level: int) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        from cards.pack.aoa.missions import MinionToMission
        world = effect.world
        if (level == 5):
            candidates = [('Protect the Professor', '45170a')]
        else:
            candidates = [(n, cid) for n, cid in MISSIONS if not CampaignLog.GetStrInternal(f'Mission Done: {n}', effect)]
        if candidates:
            name, cid = candidates[Random.RandomChoice(list(range(len(candidates))))]
            card = CardFactory.GenerateCard(cid, None, world)
            card.face.PutIntoPlay('FirstPlayer', effect)
            CampaignLog.SetStr('Current Mission', name, world)
            if (name == 'Evacuate Survivors'):
                for player in Worlds.GetPlayers(effect):
                    copy = CardFactory.GenerateCard('45178', player.player_deck, world)
                    Faces.ShuffleAllTo([copy.face], player.player_deck, effect)
            if (name == 'Sabotage the Sea Wall'):
                copy = CardFactory.GenerateCard('45177', None, world)
                Faces.ShuffleAllTo([copy.face], 'EncounterDeck', effect)
        available = [(n, cid) for n, cid in OVERSEERS if not CampaignLog.GetStrInternal(f'Overseer Defeated: {n}', effect)]
        if available:
            name, cid = available[Random.RandomChoice(list(range(len(available))))]
            card = CardFactory.GenerateCard(cid, None, world)
            MinionToMission(effect, card.face)
            CampaignLog.SetStr('Current Overseer', name, world)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def MissionTeamIntoPlay() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard('45171a,45171b', None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect, under_control=True)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def EachPlayerSearchAllyToHand() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            face = Search.PlayerCard(effect, player, include_player_deck=True, card_type=Ally)
            if face:
                Faces.AddToHand([face], player, effect)
                player.player_deck.Shuffle(effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def EachPlayerCampaignAllyIntoDeck() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card_id = CampaignLog.GetStrByPlayer('Campaign Ally', player.player_id, effect)
            if card_id:
                card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                Faces.ShuffleAllTo([card.face], player.player_deck, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def ExpertMayPlaceThreatToHeal() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        from cards.pack.aoa.missions import GetMissionScheme
        scheme = GetMissionScheme(effect)
        if (scheme == None):
            scheme = effect.this.CastTo(MainScheme)
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            def heal(targets: Sequence['CardFace']):
                scheme.PlaceThreatInternal(3, effect)
                identity.CastTo(CanHealth).HealHealth('All', effect)
            player.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility('Place 3 threat on the mission side scheme to heal to full', heal))
    return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(action)
def CampaignSetup(level: int) -> List['Ability']:
    abilities = [ShuffleApocalypseModularIntoEncounterDeck(),
                 SetupMissionAndOverseer(level),
                 MissionTeamIntoPlay(),
                 EachPlayerSearchAllyToHand(),
                 EachPlayerCampaignAllyIntoDeck(),
                 EachPlayerShufflesCopyIfPool('45178', 'Panicked Refugees'),
                 EachPlayerShufflesCopyIfPool('45176', 'Desperate Measures'),
                 ShuffleIntoEncounterIfPool('45177', 'North American Sea Wall')]
    if (level >= 2):
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(ExpertMayPlaceThreatToHeal())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect: CollectAoA(level, effect)))
    return abilities
def CollectAoA(level: int, effect: 'Effect') -> dict:
    updates = {'Current Mission': None, 'Current Overseer': None, 'Mission Result': None}
    mission = CampaignLog.GetStrInternal('Current Mission', effect)
    result = CampaignLog.GetStrInternal('Mission Result', effect)
    accomplished = (result == 'accomplished')
    if mission:
        updates[f'Mission Done: {mission}'] = '1'
        # Scenario 5 : la campagne se joue ici. Le livret (p.20) ne parle ni de
        # victoire ni de defaite mais de la mission : « If the Protect the
        # Professor MISSION side scheme was defeated, the players saved
        # Professor X and win the campaign! » Sans cette cle, l'ecran ne
        # pourrait pas distinguer une victoire sur En Sabah Nur qui sauve le
        # Professeur d'une victoire qui l'abandonne.
        if (mission == 'Protect the Professor'):
            updates['Professor Saved'] = ('1' if accomplished else None)
        if (mission == 'Liberate the Seattle Core'):
            updates['Campaign Pool: Desperate Measures'] = ('1' if accomplished else None)
        if (mission == 'Evacuate Survivors'):
            updates['Campaign Pool: Panicked Refugees'] = (None if accomplished else '1')
        if (mission == 'Sabotage the Sea Wall'):
            updates['Campaign Pool: North American Sea Wall'] = (None if accomplished else '1')
        if (mission == 'Find Lost Mutants') and (not accomplished):
            for i in range(4):
                updates[f'Player {(i + 1)} Campaign Ally'] = None
    for name, cid in OVERSEERS:
        a_id = cid.split(',')[0]
        if FaceExists(effect, a_id, in_victory=True):
            updates[f'Overseer Defeated: {name}'] = '1'
    return updates
