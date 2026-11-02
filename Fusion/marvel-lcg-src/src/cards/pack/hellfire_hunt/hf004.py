from . import *

# Divided We Fall : evenement Leadership, cout 2.
# Hero Action: Heal 1 damage from up to 2 friendly characters, If this is the first card you have played this round, give those characters a
# tough status card.
#
# Cartes de reference : 01005 (`WhenInYourPlayTurn(AbilityType.HeroAction, ...).SetPlay().SetLabel()`), `HealthUnits`, `Faces.GiveStatus`,
# `PlayerStat.this_round_played_cards` (player_stat.py).
# ⚠ « the FIRST card you have played this round » : la liste du round ne contient que CETTE carte ; « those characters » : les memes cibles.
def GetAbilities() -> Sequence['Ability']:
    def divided(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = JoueurDe(effect)
        deja = [f for f in joueur.stat.this_round_played_cards if f is not this]
        this.HealthUnits(effect.targets, 1, effect)
        if not deja:
            Faces.GiveStatus(effect.targets, "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            divided,
        ).SetPlay().SetLabel().SetTarget(Friend, range=(0, 2)),
    ]
