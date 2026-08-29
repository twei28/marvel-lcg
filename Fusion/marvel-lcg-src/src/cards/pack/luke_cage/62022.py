from . import *
def GetAbilities() -> Sequence['Ability']:
    def dynamic_duo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        import re
        player = effect.GetInitiator()
        pool = Search.SearchForCards(effect, player, include_player_deck=True, include_player_discard_pile=True)
        team_up_faces = [f for f in pool if 'Team-Up (' in (getattr(f.paper, 'text', '') or '')]
        def action(targets: Sequence['CardFace']):
            for face in targets:
                player.GainCard(face, effect)
                m = re.search(r'Team-Up \(([^)]+)\)', getattr(face.paper, 'text', '') or '')
                if m:
                    names = re.split(r'\s+and\s+', m.group(1))
                    ally_name = next((n for n in names if not (face.IsName(n) or face.IsSubName(n))), None)
                    if ally_name:
                        pool2 = Search.SearchForCards(effect, player, include_player_deck=True, include_player_discard_pile=True, name=ally_name)
                        if pool2:
                            player.GainCard(pool2[0], effect)
            player.player_deck.Shuffle(effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Choose a Team-Up card', action).SetTarget(team_up_faces, range=(0, 1)))
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, dynamic_duo).SetPlay()]
