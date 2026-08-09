from . import *

# * The Hell Charger — custom « DesignHacker » (Age of Khonshu)
# Linked (Ghost Rider) : mis en jeu par le When Defeated de 76018.
# Hero Action: Exhaust The Hell Charger and remove 1 charge counter from it →
#   your next attack this phase gains +2 ATK, piercing, and overkill.


def GetAbilities() -> Sequence['Ability']:

    def preparer_l_attaque(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        controleur = this.GetControlByPlayer()
        if controleur is None:
            return
        identite = controleur.GetIdentity()
        if identite is None:
            return

        def prochaine_attaque(effect2: 'Effect', message2: 'Message.WhenUnitWouldAttack') -> None:
            message2.GainATKForThisAttack(2, effect2)
            message2.GainPiercing(effect2)
            message2.GainOverKill(effect2)

        identite.effect.RegisterTemp(
            AbilityFactory.WhenUnitMakeAttack(
                AbilityType.ForcedInterrupt,
                "You",
                prochaine_attaque,
            ),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            preparer_l_attaque,
        ).SetName("The Hell Charger")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'charge')),
    ]
