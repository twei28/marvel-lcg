from . import *
def GetAbilities() -> Sequence['Ability']:
    def cameo(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        from cards.database import CardsDB
        this = effect.this.CastTo(Support)
        if not this.IsInPlay():
            return
        player = this.GetControlByOrOwner()
        if not Player.IsType(player):
            return
        world = this.card.world
        in_game_sets = set()
        for pl in world.players:
            for face in pl.GetAllIdentityFace():
                if face.paper.set_name:
                    in_game_sets.add(face.paper.set_name)
        hero_sets = {p.set_name for p in CardsDB.papers.values() if (p.type == 'Hero') and p.set_name}
        candidate_sets = (hero_sets - in_game_sets)
        seen = set()
        faces = []
        for card_id, paper in sorted(CardsDB.papers.items()):
            if (paper.type == 'Ally') and (paper.set_name in candidate_sets) and (paper.name not in seen):
                seen.add(paper.name)
                card = CardFactory.GenerateCard(card_id, world.area_removed, world)
                faces.append(card.face)
        if not faces:
            return
        chosen = player.AskChooseFace(faces, effect)
        if chosen:
            Faces.ShuffleAllTo([chosen], player.player_deck, effect)
        hand = list(player.hand_cards.Get())
        if hand:
            num = min(2, len(hand))
            def discard(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard 2 cards', discard).SetTarget(hand, range=(num, num), not_move=True))
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.AfterGameSetup(cameo)]
