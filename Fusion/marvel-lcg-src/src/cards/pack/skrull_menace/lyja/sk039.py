# BROUILLON (15/10/2026) : seul le « Hero Action: shuffle » est ecrit ; il manque le
# When Revealed et le Boost. Voir sk039 dans .planning/skrull-menace/transcriptions/lyja.md.
from . import *

def GetAbilities() -> Sequence['Ability']:
    def melange(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, melange).SetPlay(),
    ]
