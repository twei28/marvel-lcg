from . import *
def InPool(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(f'Campaign Pool: {name}', effect) != '')
    return check
def LogSet(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(name, effect) != '')
    return check
def PutSideSchemeIntoPlay(card_id: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def PutIntoPlayIfPool(card_id: str, pool_name: str, *, under_control: bool = False) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect, under_control=under_control)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def ShuffleIntoEncounterIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerShufflesCopyIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
            Faces.ShuffleAllTo([card.face], player.player_deck, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerNornStoneIfPool() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard('21187a,21187b', None, effect.world)
            card.SetOwner(player)
            card.face.CastTo(Upgrade).AttachTo2(player.GetIdentity(), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool('Norn Stone')])
def AvengersTowerDamagedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            identity.CastTo(Unit2).TakeDamage(effect.this, 3, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('Avengers Tower Damaged')])
def InfinityStonesCompletedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            half = (player.player_deck.GetSize() // 2)
            if (half > 0):
                Faces.DiscardAll(player.player_deck.GetTops(half), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('The Infinity Stones 1B completed')])
def ExpertMayPlaceAccelerationToHeal() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        this = effect.this.CastTo(MainScheme)
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            def heal(targets: Sequence['CardFace']):
                this.PlaceTokensInternal(1, 'acceleration_token', effect)
                identity.CastTo(CanHealth).HealHealth('All', effect)
            player.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility('Place 1 acceleration token on the main scheme to heal to full', heal))
    return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(action)
def FaceExists(effect: 'Effect', card_id: str, *, in_play: 'bool|None' = None, in_victory: 'bool|None' = None) -> bool:
    world = effect.world
    victory = world.victory_display.Get()
    for card in world.object_manager.card_dict.values():
        face = card.face
        if (face == None) or (face.paper.card_id != card_id):
            continue
        if (in_victory != None):
            if ((face in victory) != in_victory):
                continue
        if (in_play != None):
            if (face.IsInPlay() != in_play):
                continue
        return True
    return False
def ActiveMainSchemeStartswith(effect: 'Effect', prefix: str) -> bool:
    return any(s.paper.card_id.startswith(prefix) for s in Worlds.GetAllMainSchemes(effect.world))
def WriteCampaignLogAtGameOver(collect_fn) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenGameOver'):
        import json
        world = effect.world
        out = {k: v for k, v in world.store.dic.items() if isinstance(v, str)}
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            hp = (identity.health if identity else 0)
            out[f'Player {(player.player_id + 1)} Remaining hit points'] = str(max(0, hp))
            # player.GetHero() leve une AssertionError (pas None) des que le
            # joueur est cote Alter Ego, ce qui est l'etat normal en fin de
            # partie. On lit donc la face heros via GetHeroFace(), qui la
            # retrouve quelle que soit la forme active du joueur ; elle aussi
            # leve si la carte n'a vraiment aucune face heros, d'ou le garde.
            # Une identite illisible ne doit couter que sa propre cle, pas
            # faire perdre le reste du carnet.
            if identity:
                try:
                    hero_face = identity.GetHeroFace()
                except AssertionError:
                    hero_face = None
                if hero_face:
                    out[f'Player {(player.player_id + 1)} Identity'] = hero_face.paper.name.lstrip('* ')
        updates = collect_fn(effect)
        for key, value in updates.items():
            if (value == None):
                out.pop(key, None)
            else:
                out[key] = value
        try:
            with open('campaign_log_last.json', 'w') as file:
                json.dump({'players_won': message.players_won, 'suggestions': out}, file, indent=1, ensure_ascii=False)
        except OSError:
            pass
        Message.TextRender('\n--- Campaign Log (suggestions) ---', world)
        for key in sorted(out):
            Message.TextRender(f'{key} = {out[key]}', world)
    return Ability(AbilityType.Campaign, Message.WhenGameOver, [lambda e, m: Worlds.IsCampaign(e)], action)
def CollectMTS(level: int, effect: 'Effect') -> dict:
    updates = {}
    if (level == 1):
        if FaceExists(effect, '21180b', in_play=True):
            updates['Campaign Pool: Cosmo'] = '1'
        if ActiveMainSchemeStartswith(effect, '21075'):
            updates['Campaign Pool: Security Breach'] = '1'
    if (level == 2):
        if FaceExists(effect, '21182b'):
            updates['Campaign Pool: Shawarma'] = '1'
            if not FaceExists(effect, '21182b', in_victory=True):
                updates['Campaign Pool: Black Swan'] = '1'
        if FaceExists(effect, '21100b', in_play=True):
            updates['Avengers Tower Damaged'] = '1'
    if (level == 3):
        if not FaceExists(effect, '21184b', in_victory=True):
            updates['Campaign Pool: System Shock'] = '1'
        if ActiveMainSchemeStartswith(effect, '21115'):
            updates['The Infinity Stones 1B completed'] = '1'
    if (level == 4):
        if FaceExists(effect, '21186b'):
            updates['Campaign Pool: Norn Stone'] = '1'
        if FaceExists(effect, '21186b', in_victory=True):
            updates['Campaign Pool: Odin'] = '1'
    return updates
def CampaignSetup(level: int) -> List['Ability']:
    abilities = []
    if (level == 1):
        abilities.append(PutSideSchemeIntoPlay('21180a'))
        def shuffle_breach(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            card = CardFactory.GenerateCard('21181', None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
        abilities.append(AbilityFactoryCampaign.WhenCampaignSetup(shuffle_breach))
    if (level == 2):
        abilities.append(PutSideSchemeIntoPlay('21182a'))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
    if (level == 3):
        abilities.append(PutSideSchemeIntoPlay('21184a'))
        abilities.append(PutIntoPlayIfPool('21180b', 'Cosmo', under_control=True))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(PutIntoPlayIfPool('21182b', 'Black Swan'))
        abilities.append(AvengersTowerDamagedPenalty())
    if (level == 4):
        abilities.append(PutSideSchemeIntoPlay('21186a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
    if (level == 5):
        abilities.append(PutSideSchemeIntoPlay('21189a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
        abilities.append(EachPlayerNornStoneIfPool())
        abilities.append(PutIntoPlayIfPool('21139b,21139a', 'Odin', under_control=True))
    if (level >= 2):
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(ExpertMayPlaceAccelerationToHeal())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect: CollectMTS(level, effect)))
    return abilities
