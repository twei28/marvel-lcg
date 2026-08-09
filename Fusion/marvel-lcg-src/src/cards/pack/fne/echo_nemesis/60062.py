from . import *
def GetAbilities() -> Sequence['Ability']:
    def find_kingpin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        player = message.GetToPlayer()
        face = Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion)
        if not face:
            face = Search.EncounterCard(effect, include_discard_pile=True, include_set_aside=True, name='Kingpin', card_type=Minion)
            if face:
                face.PutIntoPlay(player, effect)
                return
    def boost_reveal(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        player = message.GetToPlayer()
        this.Reveal(player, effect)
    def check_kingpin_in_play(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> bool:
        return (Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion) != None)
    return [AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, CardFinder(name='Kingpin')),
            AbilityFactory.WhenThisRevealed(None, find_kingpin),
            AbilityFactory.WhenBoostCardTurnedFaceUp(AbilityType.Boost, None, boost_reveal, conditions=[check_kingpin_in_play])]
