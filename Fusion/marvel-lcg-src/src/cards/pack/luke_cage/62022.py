from . import *
def GetAbilities() -> Sequence['Ability']:
    def noms_team_up(face: 'CardFace') -> List[str]:
        import re
        groupes = getattr(face, 'team_up', None)
        if groupes and groupes[0] and groupes[1]:
            return groupes[0] + groupes[1]
        texte = getattr(face.paper, 'text', '') or ''
        m = re.search(r'Team-Up (?:<i>)?\(([^)]+)\)', texte)
        if not m:
            return []
        return re.split(r'\s+and\s+', m.group(1))

    def dynamic_duo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        player = effect.GetInitiator()

        def est_team_up(eff: 'Effect', face: 'CardFace') -> bool:
            return bool(noms_team_up(face))

        team_up = Search.PlayerCard(
            effect, player,
            include_player_deck=True,
            include_discard_pile=True,
            not_move=True,
            finder=CardFinder(check_effect_fn=est_team_up),
        )
        if team_up:
            noms = noms_team_up(team_up)

            def est_nomme(eff: 'Effect', face: 'CardFace') -> bool:
                return any(face.IsName(n) or face.IsSubName(n) for n in noms)

            allie = Search.PlayerCard(
                effect, player,
                include_player_deck=True,
                include_discard_pile=True,
                not_move=True,
                finder=CardFinder(card_type=Ally, check_effect_fn=est_nomme),
            )
            player.GainCard(team_up, effect)
            if allie:
                player.GainCard(allie, effect)
        player.player_deck.Shuffle(effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, dynamic_duo).SetPlay()]
