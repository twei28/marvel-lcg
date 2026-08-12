from . import *

# Gear Up — custom « DesignHacker »
# Hero Interrupt (defense): When you defend against an attack, you get +2 DEF
#   and gain retaliate 2 until the end of the round. After this attack is
#   resolved, change your form.
# « Until the end of the round » est rendu par GainUntilPhaseEnd : l'attaque a
# lieu pendant la phase du méchant, dont la fin coïncide avec la fin du round.


def GetAbilities() -> Sequence['Ability']:

    def gear_up(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        identite = initiator.GetIdentity()
        if identite is None:
            return

        identite.GainUntilPhaseEnd(effect, defense=2, retaliate=2)

        def apres_defense(effect2: 'Effect', message2: 'Message.AfterUnitDefendEnd') -> None:
            ChoisirEtChangerDeForme(initiator, effect2)

        identite.effect.RegisterTemp(
            AbilityFactory.AfterUnitDefendEnd(
                AbilityType.ForcedResponse,
                "You",
                apres_defense,
            ),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.HeroInterrupt,
            Enemy,
            "AnyPlayer",
            gear_up,
        ).SetPlay()
        .SetLabel('defense')
        .SetTarget("YourHero"),
    ]
