from . import *

# Traffic Jam (side scheme, 2, crisis) — [star] Hinder 2[per_hero] : base desc.
# Forced Interrupt: When a character with a VEHICLE attachment would:
#   • Add threat to a scheme, that threat is added here instead.
#   • Remove threat from a scheme, that threat is removed from here instead.
# WhenSchemeWouldPlaceThreat : PreventThreat("All") + pose ici ;
# WhenSchemeWouldRemoveThreat : SetCannotBeRemoved + retrait ici. Le personnage
# qui pose = `sch_message.trigger` (manigance) sinon `by_effect.this` ; celui
# qui retire = `by_face` (contre).

def GetAbilities() -> Sequence['Ability']:

    def pose_ici(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        valeur = message.value
        if valeur <= 0:
            return
        message.PreventThreat("All", effect)
        this.PlaceThreatOnSchemes([this], valeur, effect)

    def pose_par_un_vehicule(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> bool:
        this = effect.this
        if message.trigger is this:
            return False
        auteur = message.sch_message.trigger if message.sch_message is not None else message.by_effect.this
        return auteur is not None and AUnVehicule(auteur)

    def retire_ici(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        valeur = message.value
        message.SetCannotBeRemoved(effect)
        if valeur > 0:
            this.RemoveThreatFromSchemes([this], valeur, effect)

    def retrait_par_un_vehicule(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        this = effect.this
        if message.trigger is this:
            return False
        return message.by_face is not None and AUnVehicule(message.by_face)

    return [
        AbilityFactory.WhenSchemeWouldPlaceThreat(AbilityType.ForcedInterrupt, None, pose_ici, conditions=[pose_par_un_vehicule]),
        AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.ForcedInterrupt, None, retire_ici, conditions=[retrait_par_un_vehicule]),
    ]
