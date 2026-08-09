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
