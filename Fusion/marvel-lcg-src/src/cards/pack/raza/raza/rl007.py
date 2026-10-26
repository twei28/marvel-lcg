from . import *
def GetAbilities() -> Sequence['Ability']:
    def warrior_pride(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        joueur.DrawUp(1, effect)
        identite = IdentiteDe(effect)
        if identite is not None and identite.sustained >= SEUIL_DEGATS:
            this.HealthUnits([identite], 1, effect)
    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.HeroInterrupt,
            Villain,
            warrior_pride,
        ),
    ]
