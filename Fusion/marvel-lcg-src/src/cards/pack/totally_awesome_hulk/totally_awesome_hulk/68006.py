from . import *

# Gamma Barrier — custom « DesignHacker »
# Your hero gains retaliate 1.
# Interrupt: When you would be stunned, discard this card → prevent that stun
#   and stun the villain instead.


def GetAbilities() -> Sequence['Ability']:

    def gamma_barrier(effect: 'Effect', message: 'Message.WhenStatusWouldCardPlaceOn') -> None:
        this = effect.this.CastTo(Upgrade)

        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        # Voir 68005 : « You » et non le type `Hero`, sinon le mot-cle n'est
        # jamais applique a l'identite porteuse.
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            retaliate=1,
        ),
        AbilityFactory.WhenUnitWouldBeStatus(
            AbilityType.Interrupt,
            "You",
            ["Stunned"],
            gamma_barrier,
        ).SetTarget(Villain),
    ]
