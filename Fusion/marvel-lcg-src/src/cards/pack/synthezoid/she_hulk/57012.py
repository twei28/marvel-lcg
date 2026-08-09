from . import *
def GetAbilities() -> Sequence['Ability']:
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    def check_by_hero_or_ally(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        by = message.by_effect.this if message.by_effect else None
        return (Hero.IsType(by) or Ally.IsType(by))
    def after_change_form(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        identity = message.trigger
        Faces.ExhaustAll([identity], effect)
        this.RemoveThreatFromSchemes([this], 3, effect)
    def check_ready(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> bool:
        return message.trigger.card.state.is_ready
    return [AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove, conditions=[check_by_hero_or_ally]),
            AbilityFactory.AfterUnitChangeForm(AbilityType.AlterEgoResponse, 'You', after_change_form, to_form=AlterEgo, conditions=[check_ready])]
