from . import *
MISSION_MARK = 'mission'
def GetMissionScheme(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, card_type=EncounterSideScheme, trait='MISSION')
def GetMissionTeam(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, name='Mission Team', card_type=Support)
def GetMissionAllies(effect: 'Effect') -> List['CardFace']:
    return [x for x in Worlds.FindCardsOnField(effect, card_type=Ally) if (x.GetCounters(MISSION_MARK) > 0)]
def GetMissionMinions(effect: 'Effect') -> List['CardFace']:
    return [x for x in Worlds.FindCardsOnField(effect, card_type=Minion) if (x.GetCounters(MISSION_MARK) > 0)]
def GetIcons(face: 'CardFace') -> str:
    return str(face.paper.desc.get('RES', '') or '')
def IconsMatch(card_icons: str, ally_icons: str) -> bool:
    if (not card_icons) or (not ally_icons):
        return False
    if ('G' in card_icons) or ('G' in ally_icons):
        return True
    return any((icon in ally_icons) for icon in card_icons)
def AllyToMission(effect: 'Effect', ally: 'CardFace') -> None:
    ally.PlaceCountersInternal(1, MISSION_MARK, effect)
    ally.Gain(effect, 1, treat_as_blank=True)
    def not_count(e2: 'Effect', m2: 'Message.CheckIfAllyCountLimit') -> None:
        m2.SetNotCountAlly(e2)
    ally.effect.RegisterTemp(Ability(AbilityType.NonKeyword, Message.CheckIfAllyCountLimit, [lambda e2, m2: (m2.check_ally == ally)], not_count).NoOutOfPlayLimit(), unregister_after_exec=False, until_this_leave_play=True)
    if Player.IsType(ally.GetControlBy()):
        ally.GetControlByPlayer().limit_ally.CheckLimit([])
def MinionToMission(effect: 'Effect', minion: 'CardFace') -> None:
    if not minion.IsInPlay():
        minion.PutIntoPlay('FirstPlayer', effect)
    minion.PlaceCountersInternal(1, MISSION_MARK, effect)
    def inert(e2: 'Effect', m2: 'Message.WhenEnemyWouldActivate') -> None:
        m2.SetBeInstead(e2)
    minion.effect.RegisterTemp(AbilityFactory.WhenEnemyWouldActivate(AbilityType.NonKeyword, 'This', inert), unregister_after_exec=False, until_this_leave_play=True)
    def check_not_mission_damage(e2: 'Effect', m2: 'Message.WhenUnitWouldTakeDamage') -> bool:
        if (m2.trigger != minion):
            return False
        source = m2.source
        if source and source.IsName('Mission Team'):
            others = [x for x in GetMissionMinions(e2) if (x != minion)]
            return (len(others) > 0)
        return True
    minion.effect.RegisterTemp(AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, None, conditions=[check_not_mission_damage]), unregister_after_exec=False, until_this_leave_play=True)
CAMPAIGN_ALLIES = (('Destiny', '45172'), ('Blink', '45173'), ('Morph', '45174'), ('X-Man', '45175'))
def MissionOutcome(effect: 'Effect', scheme: 'CardFace|None', *, accomplished: bool) -> None:
    """CORRECTIF : les consequences de fin de mission n'etaient PAS implementees.

    Chaque manigance de Mission a officiellement une FACE VERSO (45166b a
    45170b) dont la « Forced Response: After you flip to this side » applique
    le resultat de la mission. Ces faces verso ne sont pas modelisees dans
    data/cards.json ; leur effet est donc simule ici, au moment exact ou la
    mission se termine. Textes officiels verifies sur marvelcdb.
    """
    if scheme is None:
        return
    cid = scheme.paper.card_id
    joueurs = Worlds.GetPlayers(effect)

    # « remove each card in the mission area from the game » : les cartes joueur
    # ont deja ete rendues a leur deck par EndMission, restent les sbires et
    # surveillants postes a la mission.
    restants = GetMissionMinions(effect)
    if restants:
        Faces.RemoveAllFromGame(restants, effect)

    def carte_en_main(player: 'Player', card_id: str) -> None:
        carte = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
        player.GainCard(carte.face, effect)

    def chercher_en_main(player: 'Player', **criteres: Any) -> None:
        face = Search.PlayerCard(effect, player, include_player_deck=True,
                                 include_discard_pile=True, may=True, **criteres)
        if face:
            player.GainCard(face, effect)

    # 45166b Liberate the Seattle Core
    if cid == '45166a':
        if accomplished:
            for player in joueurs:
                carte_en_main(player, '45176')          # Desperate Measures
        else:
            scheme.PlaceThreatOnSchemes("MainScheme", "2*", effect)
        return

    # 45167b Evacuate Survivors
    if cid == '45167a':
        for player in joueurs:
            if accomplished:
                chercher_en_main(player)
            else:
                player.DealEncounterCards(1, effect)    # face cachee
        return

    # 45168b Sabotage the Sea Wall
    if cid == '45168a':
        mur = Find.Find(effect, name='North American Sea Wall')
        if accomplished:
            if mur:
                Faces.RemoveAllFromGame([mur], effect)
            for player in joueurs:
                def frapper(targets: Sequence['CardFace']) -> None:
                    for cible in targets:
                        cible.CastTo(Unit2).TakeDamage(scheme, 3, effect)
                player.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        'Deal 3 damage to an enemy', frapper
                    ).SetTarget(Enemy, range=(1, 1)),
                )
        elif mur:
            Find.FindAndReveal(effect, Worlds.GetFirstPlayer(effect),
                               name='North American Sea Wall')
        return

    # 45169b Find Lost Mutants
    if cid == '45169a':
        for player in joueurs:
            if not accomplished:
                player.DiscardHandCards((1, 1), effect)
                continue
            choix = []
            for nom_allie, id_allie in CAMPAIGN_ALLIES:
                def fabriquer(id_allie: str, player: 'Player'):
                    def prendre(targets: Sequence['CardFace']) -> None:
                        CampaignLog.SetStr(f'Player {(player.player_id + 1)} Campaign Ally',
                                           id_allie, effect.world)
                        carte_en_main(player, id_allie)
                    return prendre
                choix.append(AbilityFactory.ForChoiceAbility(
                    f'Campaign ally: {nom_allie}', fabriquer(id_allie, player)))
            player.ChooseAbilities(effect, *choix)
        return

    # 45170b Protect the Professor
    if cid == '45170a':
        if accomplished:
            for player in joueurs:
                chercher_en_main(player, card_type=Ally)
        else:
            Worlds.SetGameOver(False, effect)
        return

def EndMission(effect: 'Effect', scheme: 'CardFace', *, accomplished: bool) -> None:
    CampaignLog.SetStr('Mission Result', ('accomplished' if accomplished else 'failed'), effect.world)
    for ally in GetMissionAllies(effect):
        owner = ally.GetControlByOrOwner()
        if Player.IsType(owner):
            Faces.ShuffleAllTo([ally], owner.player_deck, effect)
        else:
            Faces.DiscardAll([ally], effect)
    team = GetMissionTeam(effect)
    if accomplished:
        if team:
            team.card.Flip(effect)
    else:
        if team:
            Faces.RemoveAllFromGame([team], effect)
    MissionOutcome(effect, scheme, accomplished=accomplished)
    if scheme and scheme.IsInPlay():
        Faces.RemoveAllFromGame([scheme], effect)
def OverseerMissionResponse(effect: 'Effect', discarded: List['CardFace']) -> None:
    for overseer in GetMissionMinions(effect):
        cid = overseer.paper.card_id
        if (cid == '45180a'):
            num = sum((GetIcons(x).count('B')) for x in discarded)
            scheme = GetMissionScheme(effect)
            if num and scheme:
                overseer.PlaceThreatOnSchemes([scheme], (2 * num), effect)
        if (cid == '45182a'):
            num = sum((GetIcons(x).count('R')) for x in discarded)
            if num:
                overseer.CastTo(CanHealth).HealHealth((3 * num), effect)
        if (cid == '45183a'):
            num = sum((GetIcons(x).count('Y')) for x in discarded)
            allies = GetMissionAllies(effect)
            for _ in range(num):
                allies = [x for x in GetMissionAllies(effect)]
                if not allies:
                    break
                allies[0].CastTo(Unit2).TakeDamage(overseer, 1, effect)
def DoMissionAttempt(effect: 'Effect', player: 'Player') -> None:
    scheme = GetMissionScheme(effect)
    team = GetMissionTeam(effect)
    if (scheme == None) or (team == None):
        return
    allies = GetMissionAllies(effect)
    if not allies:
        return
    discarded = player.player_deck.GetTops(len(allies))
    Faces.DiscardAll(discarded, effect)
    abyss = next((x for x in GetMissionMinions(effect) if (x.paper.card_id == '45181a')), None)
    usable = list(discarded)
    if abyss:
        wilds = [x for x in usable if ('G' in GetIcons(x))]
        for face in wilds:
            Faces.MoveAllTo([face], abyss.GetInventoryDeck(), effect)
        usable = [x for x in usable if (x not in wilds)]
    OverseerMissionResponse(effect, discarded)
    sinister = any((x.paper.card_id == '45179a') for x in GetMissionMinions(effect))
    participants = []
    used_icons = set()
    remaining = list(usable)
    for ally in allies:
        for card in remaining:
            icons = GetIcons(card)
            if sinister and any((icon in used_icons) for icon in icons):
                continue
            if IconsMatch(icons, GetIcons(ally)):
                participants.append(ally)
                remaining.remove(card)
                if sinister:
                    used_icons.update(icons)
                break
    pool = sum((x.attack for x in participants))
    while (pool > 0):
        minions = GetMissionMinions(effect)
        if not minions:
            break
        minions.sort(key=lambda x: (1 if x.HasTrait('OVERSEER') else 0))
        target = minions[0]
        damage = min(pool, max(1, target.health))
        target.CastTo(Unit2).TakeDamage(team, damage, effect)
        pool -= damage
        if target.IsInPlay() and (target.health > 0):
            break
    thw = sum((x.thwart for x in participants))
    if GetMissionMinions(effect):
        thw = min(thw, max(0, (scheme.threat - 1)))
    if (thw > 0):
        scheme.RemoveThreatInternal(team, thw, effect)
    if not scheme.IsInPlay():
        EndMission(effect, scheme, accomplished=True)
        return
    if (scheme.threat <= 0):
        if not GetMissionMinions(effect):
            EndMission(effect, scheme, accomplished=True)
            return
    scheme.PlaceCountersInternal(1, MISSION_MARK, effect)
    for ally in GetMissionAllies(effect):
        ally.CastTo(Unit2).TakeDamage(scheme, 1, effect)
    if (scheme.GetCounters(MISSION_MARK) >= 4):
        EndMission(effect, scheme, accomplished=False)
