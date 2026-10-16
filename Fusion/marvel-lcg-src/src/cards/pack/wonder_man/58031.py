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
            # CORRECTIF (16/10/2026, autoplay du pack tmnt_aspect_leadership, reskin ul003) : les candidats sont
            # fabriques dans `world.area_removed`, dont le PROPRIETAIRE est le scenario (et la defausse liee celle
            # de rencontre). Melange tel quel dans le deck du joueur, l'allie choisi restait au scenario :
            # depense comme ressource, `GetControlByPlayer` levait AssertionError (3 parties sur 8). On fabrique
            # donc une copie NEUVE dans le deck du joueur (proprietaire = le joueur), puis on melange : modele
            # `skrull_menace/campaign.py` (GenerateCard(..., player.player_deck) + Shuffle).
            CardFactory.GenerateCard(chosen.paper.card_id, player.player_deck, world)
            player.player_deck.Shuffle(effect)
        hand = list(player.hand_cards.Get())
        if hand:
            num = min(2, len(hand))
            def discard(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard 2 cards', discard).SetTarget(hand, range=(num, num), not_move=True))
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.AfterGameSetup(cameo)]
