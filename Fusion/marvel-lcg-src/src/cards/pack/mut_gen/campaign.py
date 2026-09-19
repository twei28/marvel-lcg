from . import *
from cards.pack.mts.campaign import InPool, LogSet, PutIntoPlayIfPool, EachPlayerShufflesCopyIfPool, ExpertMayPlaceAccelerationToHeal, WriteCampaignLogAtGameOver, FaceExists
from engine.lib import Random
ROLE_SETS = {
    'Brawler': ['32176', '32177', '32178', '32179', '32180'],
    'Commander': ['32181', '32182', '32183', '32184', '32185'],
    'Defender': ['32186', '32187', '32188', '32189', '32190'],
    'Peacekeeper': ['32191', '32192', '32193', '32194', '32195'],
}

FUTURE_PAST_IDS = ('32166', '32167', '32168', '32169', '32170')
def SetupFuturePastDeck() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        world = effect.world
        in_victory = set(CampaignLog.GetListInternal('Future Past in Victory Display', effect))
        in_encounter = set(CampaignLog.GetListInternal('Future Past in Encounter Deck', effect))
        remaining = []
        for cid in FUTURE_PAST_IDS:
            if (cid in in_victory):
                continue
            card = CardFactory.GenerateCard(cid, None, world)
            if (cid in in_encounter):
                Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
            else:
                Faces.MoveAllTo([card.face], world.aside_deck, effect)
                remaining.append(cid)
        CampaignLog.SetStr('Future Past Deck', ';'.join(remaining), world)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def ShuffleTopFuturePastIntoEncounter(effect: 'Effect') -> None:
    from engine.lib import Random
    remaining = [x for x in CampaignLog.GetStrInternal('Future Past Deck', effect).split(';') if x]
    if not remaining:
        return
    cid = remaining[Random.RandomChoice(list(range(len(remaining))))]
    face = None
    for card in effect.world.object_manager.card_dict.values():
        if card.face and (card.face.paper.card_id == cid) and (card.area == effect.world.aside_deck):
            face = card.face
            break
    if face:
        Faces.ShuffleAllTo([face], 'EncounterDeck', effect)
    remaining.remove(cid)
    CampaignLog.SetStr('Future Past Deck', ';'.join(remaining), effect.world)
def RevealCampaignSideScheme(card_id: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.Reveal(Worlds.GetFirstPlayer(effect), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def PutRoleUpgradeIntoPlay(effect: 'Effect', player: 'Player') -> None:
    role = CampaignLog.GetStrByPlayer('Role', player.player_id, effect)
    if (role not in ROLE_SETS):
        choices = []
        chosen = {}
        for name in ROLE_SETS:
            def make(name):
                def pick(targets: Sequence['CardFace']):
                    chosen['role'] = name
                return pick
            choices.append(AbilityFactory.ForChoiceAbility(f'Role: {name}', make(name)))
        player.ChooseAbilities(effect, *choices)
        role = chosen.get('role')
        if role:
            CampaignLog.SetStr(f'Player {(player.player_id + 1)} Role', role, effect.world)
    if (role not in ROLE_SETS):
        return
    removed = CampaignLog.GetListByPlayer('Role Upgrades Removed', player.player_id, effect)
    candidates = [x for x in ROLE_SETS[role] if (x not in removed)]
    if not candidates:
        return
    card_id = Random.RandomChoice(candidates)
    card = CardFactory.GenerateCard(card_id, None, effect.world)
    card.SetOwner(player)
    face = card.face
    if Upgrade.IsType(face):
        face.CastTo(Upgrade).AttachTo2(player.GetIdentity(), effect)
        return
    face.PutIntoPlay(player, effect, under_control=True)
def EachPlayerRoleUpgrade(condition_key: 'str|None') -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            PutRoleUpgradeIntoPlay(effect, player)
    conditions = ([LogSet(condition_key)] if condition_key else [])
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)
def JubileeIntoPlay() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard('32088b,32088a', None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect)
    def check_not_removed(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal('Jubilee removed', effect) == '')
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool('Jubilee'), check_not_removed])
def ShuffleCaptiveAlliesIntoDeck() -> 'Ability':
    """Les allies liberes rejoignent un deck — celui qu'on veut, ou aucun.

    Livret p.12, 16 et 19, mot pour mot : « Each CAPTIVE ally recorded in the
    campaign log MAY be shuffled into ANY player's deck. »

    Deux libertes, et le code n'en offrait aucune : tout partait d'office chez
    le premier joueur. C'est le seul ecart de regle qui restait ouvert sur les
    huit boites. A quatre joueurs il ne s'agit pas d'un detail — les quatre
    allies du Project Wideawake se repartissent, et les entasser dans un seul
    deck le noie autant qu'il enrichit les autres.

    Un correctif avait ete ecrit puis RETIRE le 10/8/2026 : il ne posait plus
    aucun allie a la mesure. Repris et remesure le 11/8/2026, le blocage ne se
    reproduit pas, ni a un joueur ni a quatre. Il tenait tres probablement a la
    facon dont la question etait posee, pas a l'idiome lui-meme.

    Une carte n'est fabriquee qu'une fois le deck CHOISI : un refus ne doit
    laisser trainer aucun exemplaire hors jeu.

    ET ELLE EST FABRIQUEE HORS DECK. `Faces.ShuffleAllTo` ne melange QUE s'il a
    deplace quelque chose (`if moved_faces: deck.Shuffle(...)`). La generer
    directement dans `player_deck`, comme le faisait le code d'origine, ne
    deplacait donc rien : le melange ne partait jamais et les allies restaient
    sur le dessus. Mesure a l'appui, avant correction : les QUATRE captifs se
    retrouvaient dans la main de depart, a un joueur comme a deux. Le livret
    dit « shuffled into », pas « posed on top of ».
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card_ids = CampaignLog.GetListInternal('Captive Allies', effect)
        if not card_ids:
            return
        premier = Worlds.GetFirstPlayer(effect)
        joueurs = Worlds.GetPlayers(effect)

        for card_id in card_ids:
            papers = CardFactory.FindCardPapers(card_id)
            nom = papers[0].name if papers else card_id

            def ranger(joueur: 'Player', identifiant: str):
                def poser(targets: 'Sequence[CardFace]'):
                    card = CardFactory.GenerateCard(identifiant, None, effect.world)
                    Faces.ShuffleAllTo([card.face], joueur.player_deck, effect)
                return poser

            choix = []
            for joueur in joueurs:
                identite = joueur.GetIdentity()
                porteur = identite.name if identite else f'Player {joueur.player_id + 1}'
                choix.append(AbilityFactory.ForChoiceAbility(
                    f"Shuffle {nom} into {porteur}'s deck",
                    ranger(joueur, card_id),
                ))
            # MayChooseOneAbility et non ChooseAbilities : le livret dit « may »,
            # donc l'equipe doit pouvoir laisser un allie de cote.
            premier.MayChooseOneAbility(effect, *choix)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def CampaignSetup(level: int) -> List['Ability']:
    abilities = [SetupFuturePastDeck()]
    if (level == 1):
        abilities.append(EachPlayerRoleUpgrade(None))
        abilities.append(RevealCampaignSideScheme('32171a,32171b'))
    if (level == 2):
        abilities.append(EachPlayerRoleUpgrade('Frightened Police Defeated'))
        abilities.append(RevealCampaignSideScheme('32172a,32172b'))
    if (level >= 3):
        abilities.append(JubileeIntoPlay())
        abilities.append(ShuffleCaptiveAlliesIntoDeck())
    if (level == 3):
        abilities.append(EachPlayerRoleUpgrade('Enemy of My Enemy Defeated'))
        abilities.append(RevealCampaignSideScheme('32173a,32173b'))
    if (level == 4):
        abilities.append(EachPlayerRoleUpgrade('Find the Prisoners Defeated'))
        abilities.append(RevealCampaignSideScheme('32174a,32174b'))
    if (level == 5):
        abilities.append(EachPlayerRoleUpgrade('Surprise Attack Defeated'))
        abilities.append(RevealCampaignSideScheme('32175a,32175b'))
    if (level >= 2):
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(ExpertMayPlaceAccelerationToHeal())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect, message: CollectMG(level, effect)))
    return abilities
def CollectMG(level: int, effect: 'Effect') -> dict:
    updates = {}
    flips = {1: ('32171b', 'Frightened Police Defeated'),
             2: ('32172b', 'Enemy of My Enemy Defeated'),
             3: ('32173b', 'Find the Prisoners Defeated'),
             4: ('32174b', 'Surprise Attack Defeated')}
    if (level in flips):
        flip_id, key = flips[level]
        if FaceExists(effect, flip_id):
            updates[key] = '1'
    all_role_ids = {x for ids in ROLE_SETS.values() for x in ids}
    area_removed = effect.world.area_removed
    for player in Worlds.GetPlayers(effect):
        used = set()
        for card in effect.world.object_manager.card_dict.values():
            face = card.face
            if face and (face.paper.card_id in all_role_ids) and (face.card.area == area_removed):
                if (face.GetControlByOrOwner() == player):
                    used.add(face.paper.card_id)
        if used:
            existing = set(CampaignLog.GetListByPlayer('Role Upgrades Removed', player.player_id, effect))
            updates[f'Player {(player.player_id + 1)} Role Upgrades Removed'] = ';'.join(sorted(existing | used))
    in_victory = set(CampaignLog.GetListInternal('Future Past in Victory Display', effect))
    in_encounter = set(CampaignLog.GetListInternal('Future Past in Encounter Deck', effect))
    for cid in FUTURE_PAST_IDS:
        if (cid in in_victory):
            continue
        if FaceExists(effect, cid, in_victory=True):
            in_victory.add(cid)
            in_encounter.discard(cid)
        else:
            for card in effect.world.object_manager.card_dict.values():
                if card.face and (card.face.paper.card_id == cid) and (card.area != effect.world.aside_deck):
                    in_encounter.add(cid)
                    break
    updates['Future Past in Victory Display'] = (';'.join(sorted(in_victory)) or None)
    updates['Future Past in Encounter Deck'] = (';'.join(sorted(in_encounter)) or None)
    updates['Future Past Deck'] = None
    # CORRECTIF (10/8/2026) : le carnet officiel (mc32_mutant_genesis_campaign_log.pdf)
    # porte DEUX lignes d'allies, pas une. « Allies from Abduction Protocols »
    # au scenario 2, et « Allies under Rescue Captives or Find the Prisoners »
    # au scenario 3. Le moteur ne relevait que le niveau 2 : les allies liberes
    # au scenario 3 sous Rescue Captives (32173b, qui les rend a chaque
    # SENTINEL vaincu) etaient perdus, alors que la mise en place des scenarios
    # 4 et 5 dit « each CAPTIVE ally recorded in the campaign log may be
    # shuffled into any player's deck ». Les deux lignes du carnet alimentent
    # la meme etape, une seule cle suffit donc, mais il faut la nourrir aux
    # deux niveaux. Le set s'unit a l'existant, rien n'est ecrase.
    if (level in (2, 3)):
        captives = set(CampaignLog.GetListInternal('Captive Allies', effect))
        for card in effect.world.object_manager.card_dict.values():
            face = card.face
            if face and face.IsInPlay() and face.HasTrait('CAPTIVE') and Ally.IsType(face):
                captives.add(face.paper.card_id)
        if captives:
            updates['Captive Allies'] = ';'.join(sorted(captives))
    if FaceExists(effect, '32088b', in_play=True):
        updates['Campaign Pool: Jubilee'] = '1'
    elif (CampaignLog.GetStrInternal('Campaign Pool: Jubilee', effect) != ''):
        updates['Campaign Pool: Jubilee'] = None
        updates['Jubilee removed'] = '1'
    return updates
