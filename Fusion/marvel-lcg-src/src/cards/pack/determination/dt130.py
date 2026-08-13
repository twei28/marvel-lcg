from . import *

# Timed Detonation

def GetAbilities() -> Sequence['Ability']:

    def timed_detonation(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        ennemi = this.GetBindFace()
        if player is not None:
            player.GetIdentity().ChangeToForm(AlterEgo, effect)
        Faces.RemoveAllFromGame([this], effect)
        if ennemi is not None:
            this.DealDamage([ennemi], 6, effect,
                            property=AttackProperty(ranged=True, overkill=True))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Enemy)
        ),
        AbilityFactory.WhenPhaseEnd(
            AbilityType.ForcedInterrupt,
            "Villain",
            timed_detonation
        ),
    ]
