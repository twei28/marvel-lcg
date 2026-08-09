from . import *
def GetAbilities() -> Sequence['Ability']:
    def after_activate(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Minion)
        if not PlaceThreatOnAllVersusAll(effect, this, 2):
            this.PlaceThreatOnSchemes('MainScheme', 1, effect)
    return [AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, 'This', after_activate),
            AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, 'This', after_activate)]
