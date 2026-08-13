from . import *

# Divert Attention

def GetAbilities() -> Sequence['Ability']:

    def check_side_scheme_en_victoire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        tableau = Worlds.VictoryDisplay(effect)
        return any(Scheme2.IsType(f) for f in tableau.GetAll()) if tableau else False

    def divert_attention(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        source = effect.targets[0] if effect.targets else None
        if source is None:
            return
        autres = [s for s in Worlds.GetOnFieldSchemes(effect) if s is not source]
        if not autres:
            return

        # « aussi egalement que possible » : on retire d'abord, puis on repose en
        # tournant sur les manigances, ce qui donne le partage le plus egal.
        total = min(6, source.CastTo(Scheme2).threat)
        retire = this.RemoveThreatFromSchemes([source], total, effect) or 0
        for i in range(retire):
            this.PlaceThreatOnSchemes([autres[i % len(autres)]], 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            divert_attention,
            conditions=[check_side_scheme_en_victoire],
        ).SetPlay()
        .SetTarget(Scheme2),
    ]
