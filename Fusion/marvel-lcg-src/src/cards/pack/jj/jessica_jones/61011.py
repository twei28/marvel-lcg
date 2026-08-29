from . import *
def GetAbilities() -> Sequence['Ability']:
    def after_defend(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
        if alias:
            alias.PlaceCountersInternal(1, 'evidence', effect)
    return [
        *AbilityFactory.GiveKeywordToAttached(Hero, defense=2),
        AbilityFactory.AfterUnitDefendAgainstAttack(AbilityType.Response, "You", after_defend),
    ]
