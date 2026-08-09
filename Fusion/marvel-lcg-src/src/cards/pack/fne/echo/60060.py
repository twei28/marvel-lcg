from . import *
def GetAbilities() -> Sequence['Ability']:
    def raised_by_the_kingpin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        player = this.GetGaveToPlayer() or message.GetToPlayer()
        face = Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion)
        if not face:
            face = Search.EncounterCard(effect, include_discard_pile=True, include_set_aside=True, name='Kingpin', card_type=Minion)
            if face:
                face.PutIntoPlay(player, effect)
                return
    def after_thwart(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Obligation)
        num = message.remove_threat
        if (num > 0):
            this.PlaceCountersInternal(num, 'all-purpose', effect)
        if (this.GetAllCounters() >= 4):
            Faces.RemoveAllFromGame([this], effect)
    def check_you(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> bool:
        this = effect.this.CastTo(Obligation)
        return (message.trigger.GetControlBy() == this.GetGaveToPlayer())
    def check_source_yours(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Obligation)
        source = message.source
        if (source == None):
            return False
        return (source.GetControlBy() == this.GetGaveToPlayer())
    return [AbilityFactory.WhenThisRevealed(None, raised_by_the_kingpin),
            AbilityFactory.AfterUnitThwartScheme(AbilityType.Response, None, None, after_thwart, remove_threat=True, conditions=[check_you]),
            AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, CardFinder(name='Kingpin', card_type=Minion), conditions=[check_source_yours])]
