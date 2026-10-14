from cards.pack import *
GIFT_IDS = ('59005', '59006', '59007')
LABOR_IDS = ('59002', '59003', '59004')
def CountGifts(effect: 'Effect', player: 'Player') -> int:
    if player.obligations_area.FindCard(name='Appeal to Athena'):
        return 0
    count = 0
    for face in Worlds.FindCardsOnField(effect, trait='GIFT'):
        if (face.GetControlByPlayer() == player):
            count += 1
    return count
def GetAdditionalDeckTop(player: 'Player', trait: 'CardFace.TRAITS') -> 'CardFace|None':
    for face in player.additional_deck.Get(True):
        if face.HasTrait(trait):
            return face
    return None
def PutTopGiftIntoPlay(effect: 'Effect', player: 'Player') -> None:
    face = GetAdditionalDeckTop(player, 'GIFT')
    if face:
        face.CastTo(Upgrade).PutIntoPlay(player, effect, under_control=True)
def JoueurHercules(effect: 'Effect') -> 'Player|None':
    """Le joueur qui joue Hercules : une Labor attachee a un sbire n'a pas de controleur joueur."""
    for candidat in Worlds.GetPlayers(effect):
        identite = candidat.GetIdentity()
        if identite and identite.IsName('Hercules'):
            return candidat
    return None
def RemettreSousLeDeckLabor(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
    """RR 1.8 FAQ (Hercules) : « Any time a Labor card leaves play other than being placed in the
    victory display, place it on the bottom of the Labor deck. » Sans limite : a CHAQUE sortie."""
    this = effect.this
    if this.card.area.flags.is_victory_display:
        return
    player = JoueurHercules(effect)
    if player is None:
        return
    Faces.FlipAllTo([this], False, effect)
    this.card.MoveToBottom(player.additional_deck, effect)
def CapaciteRetourAuDeckLabor() -> 'Ability':
    return AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, 'This', RemettreSousLeDeckLabor)
def Atonement(effect: 'Effect', player: 'Player') -> None:
    world = effect.world
    key = f'AtonementUsedThisPhase P{player.player_id}'
    if world.store.HasKey(key) and world.store.GetStr(key):
        return
    world.store.SetStr(key, '1')
    def clear_flag():
        world.store.SetStr(key, '')
    RunAt.TheEndOfThePhase(effect, clear_flag)
    PutTopGiftIntoPlay(effect, player)
    identity = player.GetIdentity()
    Faces.ReadyAll([identity], effect)
    if player.IsInHeroForm():
        YouMayFlipToYourAlterEgoForm(player, effect)
