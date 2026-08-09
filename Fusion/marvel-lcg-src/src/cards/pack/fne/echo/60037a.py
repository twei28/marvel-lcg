from . import *
def GetAbilities() -> Sequence['Ability']:
    def watch_and_learn(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        controller = this.GetControlByPlayer()
        face = message.played_face
        if not (face.card.area.flags.is_discards or face.IsInProcessingArea()):
            return
        this.TuckCardUnderHere(face, effect)
        placed = this.GetPlacedCardArea().Get()
        excess = (len(placed) - 3)
        if (excess > 0):
            def action(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            controller.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard tucked cards down to 3', action).SetTarget(list(placed), range=(excess, excess), not_move=True))
    def check_aspect_event(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        face = message.played_face
        if not IsAspectOrBasicEvent(face):
            return False
        return (message.from_area != effect.this.GetPlacedCardArea())
    def check_tucked_playable(effect: 'Effect', message: 'Message.CheckIfFaceIsLikeInHand') -> bool:
        this = effect.this
        face = message.which_face
        if (face.card.area != this.GetPlacedCardArea()):
            return False
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        if (initiator != this.GetControlByPlayer()):
            return False
        if not initiator.IsInHeroForm():
            return False
        return (initiator.hand_cards.FindCard(name='Photographic Reflexes') != None)
    def discard_photographic_reflexes(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this
        player = this.GetControlByPlayer()
        prs = [x for x in player.hand_cards.Get() if x.IsName('Photographic Reflexes')]
        if not prs:
            return
        if (len({x.paper.card_id for x in prs}) <= 1):
            Faces.DiscardAll([prs[0]], effect)
            return
        def action(targets: Sequence['CardFace']):
            Faces.DiscardAll(list(targets), effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a Photographic Reflexes', action).SetTarget(prs, range=(1, 1), not_move=True))
    def check_played_from_tuck(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        return (message.from_area == effect.this.GetPlacedCardArea())
    def check_pay_for_tucked(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        this = effect.this
        paying_face = message.paying_for_effect.this
        if (paying_face.card.area != this.GetPlacedCardArea()):
            return False
        player = message.GetToPlayer()
        if (player != this.GetControlByPlayer()):
            return False
        return (player.hand_cards.FindCard(name='Photographic Reflexes') != None)
    return [AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'AnyPlayer', None, watch_and_learn, conditions=[check_aspect_event]).SetName('Watch and Learn'),
            *AbilityFactory.YouMayPlayCardLikeInHand(AbilityType.NonKeyword, None, conditions=[check_tucked_playable]),
            AbilityFactory.WhenPlayerPlayCard(AbilityType.Rule, 'You', None, discard_photographic_reflexes, conditions=[check_played_from_tuck]),
            AbilityFactory.CanGenerateResources(AbilityType.Resource, Resources('GG'), is_play_card=True, conditions=[check_pay_for_tucked])]
