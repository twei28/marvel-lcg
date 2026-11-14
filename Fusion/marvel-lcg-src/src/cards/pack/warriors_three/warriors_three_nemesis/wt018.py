from . import *


def GetAbilities() -> Sequence['Ability']:
    def seulement_fenris(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        source = getattr(getattr(message, "by_effect", None), "this", None)
        if source is None or not source.IsName("Fenris"):
            message.PreventThreat("All", effect)

    def fin_du_monde(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        Unused(message)
        if effect.this.threat >= 5:
            Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile("This"),
        AbilityFactory.WhenThreatWouldBePlacedOn(AbilityType.ForcedInterrupt, "This", seulement_fenris),
        AbilityFactory.AfterSchemePlaceThreat(AbilityType.ForcedResponse, "This", fin_du_monde),
    ]
