from . import *
from cards.pack.synthezoid import EarnLeaderBasicCards, GetSetAsideLeaderBasics
def GetAbilities() -> Sequence['Ability']:
    def choosing_sides(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        for player in Worlds.GetPlayers(effect):
            player.DealEncounterCards(1, effect)
        if (this.card.back_faces != []):
            this.card.Flip(effect)
    return [AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, CardFinder(card_type=Leader), cannot_take_more_than_damage=2, is_from_attack=True),
            AbilityFactory.AfterSchemeRemoveThreat(AbilityType.ForcedResponse, 'This', choosing_sides, last_threat=True)]
