from . import *
def GetAbilities() -> Sequence['Ability']:
    def gather_evidence(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
        if alias:
            alias.PlaceCountersInternal(1, 'evidence', effect)
    return [AbilityFactory.AfterUnitUseBasicPower(AbilityType.Response, "You", gather_evidence)]
