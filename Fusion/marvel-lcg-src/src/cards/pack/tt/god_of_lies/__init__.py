# Complété pour le scénario God of Lies jouable (adaptation 1 groupe).
# Le stub d'origine PlaceShatterCountersOnTheAvatarOfLokivillain(size) était vide (pass).

from cards.pack import *
AVATAR_TRAIT = 'AVATAR OF LOKI'
AVATAR_SYNERGY = {'Loki the Rascal': 'Unified Front',
                  'Loki the Miscreant': 'Mounting Resistance',
                  'Loki the Knave': 'Domineering Force',
                  'Loki the Wretch': 'Feigned Retreat'}
def FindAvatarOfLoki(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, trait=AVATAR_TRAIT, card_type=Villain)
def FindGodOfLies(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, name='Loki, God of Lies', card_type=Villain)
def GetSetAsideAvatars(effect: 'Effect') -> List['Villain']:
    faces = ([x for x in Worlds.GetSetAsideAreaCards(effect) if Villain.IsType(x)] + Worlds.GetScenario(effect).villain_deck.Get())
    villains = CardFinder(trait=AVATAR_TRAIT, card_type=Villain).Checks(faces)
    return villains
def PlaceShatterCountersOnTheAvatarOfLokivillain(size: int, effect: 'Effect|None' = None):
    if effect is None:
        return
    avatar = FindAvatarOfLoki(effect)
    if avatar:
        Faces.PlaceCountersOn([avatar], size, 'shatter', effect)
def PlaceSynergyCounters(env_name: str, size: int, effect: 'Effect'):
    face = Worlds.FindCardOnField(effect, name=env_name, card_type=Environment)
    if not face:
        return
    cap = Worlds.GetPlayerNumIcon(effect)
    current = face.CastTo(CanPlaceCounter).GetCounters('synergy')
    size = min(size, max(0, (cap - current)))
    if (size > 0):
        Faces.PlaceCountersOn([face], size, 'synergy', effect)
def CheckGodOfLiesFlip(effect: 'Effect'):
    gol = FindGodOfLies(effect)
    if not gol:
        return
    if (gol.paper.card_id != '55027a'):
        return
    limit = (10 * Worlds.GetPlayerNumIcon(effect))
    if (gol.CastTo(CanHealth).health > limit):
        return
    gol.card.Flip(effect)
    avatar = FindAvatarOfLoki(effect)
    focus = None
    for face in Worlds.GetSetAsideAreaCards(effect):
        if (face.paper.name == 'Intense Focus'):
            focus = face
            break
    if not focus:
        focus = Worlds.FindCardOnField(effect, name='Intense Focus')
    if focus and avatar:
        if Worlds.IsExpert(effect) and (focus.paper.card_id == '55034a'):
            focus.card.Flip(effect)
            focus = focus.card.face
        if not focus.IsInPlay():
            focus.CastTo(Attachment).AttachTo2(avatar, effect)
        Worlds.DiscardEncounterCards('2*', effect)
        if Worlds.IsExpert(effect):
            first_player = Worlds.GetFirstPlayer(effect)
            scepter = Search.EncounterCard(effect, first_player, include_discard_pile=True, name='Dark Scepter')
            if scepter:
                scepter.Reveal(first_player, effect)
            else:
                Faces.GiveStatus([avatar], 'Tough', effect)
        def action(player: 'Player'):
            for _ in range(5):
                top = player.player_deck.GetTop()
                if top:
                    Faces.DiscardAll([top], effect)
        Players.ForEachPlayer(effect, action)
def ShatterTheIllusion(avatar: 'CardFace', env_name: str, effect: 'Effect'):
    counters = avatar.CastTo(CanPlaceCounter).GetCounters('shatter')
    gol = FindGodOfLies(effect)
    if gol and (counters > 0):
        gol.CastTo(CanHealth).TakeDamageNoDeath(avatar, counters, effect)
        gol2 = FindGodOfLies(effect)
        if (gol2 == None) or (gol2.CastTo(CanHealth).health <= 0):
            Worlds.SetGameOver(True, effect)
            return
        CheckGodOfLiesFlip(effect)
    PlaceSynergyCounters(env_name, Worlds.GetPlayerNumIcon(effect), effect)
    avatar.CastTo(CanPlaceCounter).SetCounters(0, 'shatter', effect)
def AvatarWouldBeDefeated(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
    this = effect.this.CastTo(Villain)
    message.SetBeInstead(effect)
    this.ResetHealth(effect)
    num = (5 * Worlds.GetPlayerNumIcon(effect))
    Faces.PlaceCountersOn([this], num, 'shatter', effect)
    env_name = AVATAR_SYNERGY.get(this.paper.name, 'Unified Front')
    ShatterTheIllusion(this, env_name, effect)
    others = [x for x in GetSetAsideAvatars(effect) if (x.card != this.card)]
    if others:
        new_avatar = Rand.RandomChoice(others, effect)
        this.card.SwapCard(new_avatar, effect)
def WhenDefeatedPlaceShatterCountersOnTheAvatarOfLokivillain(size: int, action: Callable[(['Effect', 'Message.WhenUnitBeDefeated'], None)] | None = None) -> 'Ability':
    def grendell_defeated(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        PlaceShatterCountersOnTheAvatarOfLokivillain(size, effect)
        if action:
            action(effect, message)
            return
    return AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, 'This', grendell_defeated)
