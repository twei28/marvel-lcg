from . import *
def GetAbilities() -> Sequence['Ability']:
    def internal_injury(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Obligation)
        player = this.GetGaveToPlayer()
        identity = player.GetIdentity() if player else None
        if identity:
            this.DealDamage(
                [identity],
                # CORRECTIF (12/09/2026) : « take 3 **unpreventable** damage ».
                # `ignore_tough` seul ne fermait qu'une porte sur trois : la carte
                # Coriace. Une prevention chiffree (08032 Defensive Stance) ou un
                # remplacement (49006 Magnetic Bubble) passaient au travers.
                # `DamageProperty.unpreventable`, ajoute pour le pack `sentinel`,
                # ferme les trois.
                DamageProperty(damage=3, ignore_tough=True, unpreventable=True),
                effect)
    def after_recover(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.RemoveAllFromGame([this], effect)
    return [
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Player", internal_injury),
        AbilityFactory.AfterUnitRecovery(AbilityType.AlterEgoResponse, "You", after_recover),
    ]
