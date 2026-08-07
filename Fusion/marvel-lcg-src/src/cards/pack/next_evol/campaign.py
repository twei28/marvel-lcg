from . import *
from cards.pack.mts.campaign import InPool, LogSet, ExpertMayPlaceAccelerationToHeal, WriteCampaignLogAtGameOver, FaceExists
CAMPAIGN_SCHEMES = [
    ('Assemble the Team', '40190a,40190b', '40199'),
    ('Establish Safehouse', '40191a,40191b', '40201'),
    ('Gear Up', '40192a,40192b', '40203'),
    ('Mission Prep', '40193a,40193b', '40200'),
    ('Practice Maneuvers', '40194a,40194b', '40198'),
    ('Prepare Defenses', '40195a,40195b', '40202'),
]
ENVIRONMENTS = {
    'Team Assembled': '40190b,40190a',
    'Safehouse Established': '40191b,40191a',
    'Geared Up': '40192b,40192a',
    'Mission Prepped': '40193b,40193a',
    'Practiced Maneuvers': '40194b,40194a',
    'Prepared Defenses': '40195b,40195a',
}
ENV_B_IDS = ('40190b', '40191b', '40192b', '40193b', '40194b', '40195b')
def CampaignEnvsInPlay(effect: 'Effect') -> List['CardFace']:
    faces = []
    for card in effect.world.object_manager.card_dict.values():
        face = card.face
        if face and face.IsInPlay() and (face.paper.card_id in ENV_B_IDS):
            faces.append(face)
    return faces
def ShuffleEncounterCard(effect: 'Effect', card_id: str) -> None:
    card = CardFactory.GenerateCard(card_id, None, effect.world)
    Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
def ChooseCampaignPlayerSideScheme() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        player = Worlds.GetFirstPlayer(effect)
        choices = []
        for name, scheme_id, enc_id in CAMPAIGN_SCHEMES:
            if CampaignLog.GetStrInternal(f'Removed: {name}', effect):
                continue
            if CampaignLog.GetStrInternal(f'Chose: {name}', effect):
                continue
            def make(name, scheme_id, enc_id):
                def pick(targets: Sequence['CardFace']):
                    card = CardFactory.GenerateCard(scheme_id, None, effect.world)
                    card.face.not_count_player_side_scheme_limit = True
                    card.face.PutIntoPlay(player, effect)
                    ShuffleEncounterCard(effect, enc_id)
                    CampaignLog.SetStr(f'Chose: {name}', '1', effect.world)
                return pick
            choices.append(AbilityFactory.ForChoiceAbility(f'Put "{name}" into play', make(name, scheme_id, enc_id)))
        if choices:
            player.ChooseAbilities(effect, *choices)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def PutEarnedEnvironmentsIntoPlay() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        player = Worlds.GetFirstPlayer(effect)
        for name, card_id in ENVIRONMENTS.items():
            if CampaignLog.GetStrInternal(f'Campaign Pool: {name}', effect):
                card = CardFactory.GenerateCard(card_id, None, effect.world)
                card.face.PutIntoPlay(player, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def ShuffleChosenEncounterCards() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for name, scheme_id, enc_id in CAMPAIGN_SCHEMES:
            if CampaignLog.GetStrInternal(f'Chose: {name}', effect):
                ShuffleEncounterCard(effect, enc_id)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def RemoveMaraudersDefeatedBeforeSetup() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCardSetup'):
        names = CampaignLog.GetListInternal('Marauders Defeated', effect)
        if not names:
            return
        wanted = {str(x).strip().lstrip('* ').lower() for x in names}
        villain_deck = Worlds.GetScenario(effect).villain_deck
        to_remove = [f for f in villain_deck.GetAll() if (f.paper.name.lstrip('* ').lower() in wanted) or (f.paper.card_id in wanted)]
        if to_remove:
            Faces.RemoveAllFromGame(to_remove, effect)
    def check_before(effect: 'Effect', message: 'Message.WhenCardSetup') -> bool:
        if (effect.this != message.trigger):
            return False
        return message.before_put_setup_cards
    return Ability(AbilityType.Campaign, Message.WhenCardSetup, [check_before, lambda e, m: Worlds.IsCampaign(e)], action)
def MorlocksSavedSearch() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        num = CampaignLog.GetIntInternal('Morlocks Saved', effect)
        if (num <= 0):
            return
        players = Worlds.GetPlayers(effect)
        for i in range(num):
            player = players[i % len(players)]
            face = Search.PlayerCard(effect, player, include_player_deck=True)
            if face:
                Faces.AddToHand([face], player, effect)
        for player in players:
            player.player_deck.Shuffle(effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def GiveEnemiesToughIfEnvEarned() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        if not CampaignEnvsInPlay(effect):
            return
        for enemy in Worlds.FindCardsOnField(effect, card_type=Enemy):
            Faces.GiveStatus([enemy], 'Tough', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def JuggernautMomentumCounters() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        num = len(CampaignEnvsInPlay(effect))
        if (num <= 0):
            return
        for villain in Worlds.GetAllVillains(effect):
            villain.PlaceCountersInternal(num, 'momentum', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def DealBlackTomAndCreepingWillows() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        from engine.lib import Random
        players = Worlds.GetPlayers(effect)
        encounter_deck = Worlds.GetEncounterDeck(effect)
        cards = []
        tom = encounter_deck.FindCard(name='Black Tom Cassidy')
        if tom:
            cards.append(tom)
        willows = encounter_deck.FindCards(name='Creeping Willow', max=len(players))
        cards += willows
        if not cards:
            return
        order = list(range(len(cards)))
        for i in range(len(order) - 1, 0, -1):
            j = Random.RandomChoice(list(range(i + 1)))
            order[i], order[j] = order[j], order[i]
        for idx, player in enumerate(players):
            if (idx >= len(order)):
                break
            face = cards[order[idx]]
            Faces.FlipAllTo([face], False, effect)
            Faces.MoveAllTo([face], player.dealt_encounter_cards, effect)
        encounter_deck.Shuffle(effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def HopeDamageChoice(scenario_key: str, scheme_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        damage = CampaignLog.GetIntInternal(scenario_key, effect)
        if (damage <= 0):
            return
        player = Worlds.GetFirstPlayer(effect)
        hope = Worlds.FindCardOnField(effect, name='Hope Summers', card_type=Ally)
        scheme = Worlds.FindCardOnField(effect, name=scheme_name)
        choices = []
        if hope:
            choices.append(AbilityFactory.ForChoiceAbility(f'Place {damage} damage on Hope Summers', lambda targets: hope.CastTo(Unit2).TakeDamage(hope, damage, effect)))
        if scheme:
            choices.append(AbilityFactory.ForChoiceAbility(f'Place {damage} threat on {scheme_name}', lambda targets: scheme.PlaceThreatInternal(damage, effect)))
        if choices:
            player.ChooseAbilities(effect, *choices)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def TeleportedAwaySetup() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        scheme = Worlds.FindCardOnField(effect, name='Teleported Away')
        if (scheme == None):
            encounter_deck = Worlds.GetEncounterDeck(effect)
            scheme = encounter_deck.FindCard(name='Teleported Away')
            if scheme:
                scheme.PutIntoPlay('FirstPlayer', effect)
        if scheme:
            num = len(CampaignEnvsInPlay(effect))
            if (num > 0):
                scheme.PlaceThreatInternal((num * len(Worlds.GetPlayers(effect))), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def StryfesGraspThreat() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        scheme = Worlds.FindCardOnField(effect, name="Stryfe's Grasp")
        if scheme:
            num = len(CampaignEnvsInPlay(effect))
            if (num > 0):
                scheme.PlaceThreatInternal((num * len(Worlds.GetPlayers(effect))), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def EachPlayerDiscardUntilPsionic() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        encounter_deck = Worlds.GetEncounterDeck(effect)
        for player in Worlds.GetPlayers(effect):
            found = None
            guard = 0
            while (guard < 80):
                guard += 1
                top = encounter_deck.GetTop()
                if (top == None):
                    break
                Faces.DiscardAll([top], effect)
                if Minion.IsType(top) or (Attachment.IsType(top) and top.HasTrait('PSIONIC')):
                    found = top
                    break
            if found:
                found.Reveal(player, effect)
        encounter_deck.ShuffleWithDiscardPile(False, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def CollectNeXt(level: int, effect: 'Effect') -> dict:
    updates = {}
    env_names = {'40190a': 'Team Assembled', '40191a': 'Safehouse Established', '40192a': 'Geared Up',
                 '40193a': 'Mission Prepped', '40194a': 'Practiced Maneuvers', '40195a': 'Prepared Defenses'}
    for name, scheme_id, enc_id in CAMPAIGN_SCHEMES:
        a_id = scheme_id.split(',')[0]
        b_id = (a_id[:-1] + 'b')
        if FaceExists(effect, b_id, in_play=True):
            updates[f'Campaign Pool: {env_names[a_id]}'] = '1'
        if FaceExists(effect, a_id, in_play=True):
            updates[f'Removed: {name}'] = '1'
    if (level in (3, 4)):
        hope = Worlds.FindCardOnField(effect, name='Hope Summers', card_type=Ally)
        if hope:
            damage = max(0, (3 - max(0, hope.health)))
            updates[f"Hope Summers's Damage Scenario {level}"] = str(damage)
    return updates
def CampaignSetup(level: int) -> List['Ability']:
    abilities = [PutEarnedEnvironmentsIntoPlay()]
    if (level == 2):
        abilities.append(RemoveMaraudersDefeatedBeforeSetup())
        abilities.append(MorlocksSavedSearch())
        abilities.append(GiveEnemiesToughIfEnvEarned())
    if (level == 3):
        abilities.append(JuggernautMomentumCounters())
        abilities.append(DealBlackTomAndCreepingWillows())
    if (level == 4):
        abilities.append(TeleportedAwaySetup())
        abilities.append(HopeDamageChoice("Hope Summers's Damage Scenario 3", 'Teleported Away'))
    if (level == 5):
        abilities.append(StryfesGraspThreat())
        abilities.append(HopeDamageChoice("Hope Summers's Damage Scenario 4", "Stryfe's Grasp"))
        abilities.append(EachPlayerDiscardUntilPsionic())
    abilities.append(ShuffleChosenEncounterCards())
    abilities.append(ChooseCampaignPlayerSideScheme())
    if (level >= 2):
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        if (level in (3, 5)):
            abilities.append(AbilityFactoryCampaign.ExpertCampaignEachPlayerMayDealFacedownEncounterCardYpHealHP(1))
        else:
            abilities.append(ExpertMayPlaceAccelerationToHeal())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect: CollectNeXt(level, effect)))
    return abilities
