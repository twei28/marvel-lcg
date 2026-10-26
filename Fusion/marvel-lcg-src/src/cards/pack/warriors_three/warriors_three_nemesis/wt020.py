from . import *


def GetAbilities() -> Sequence['Ability']:
    def devient_allie(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        # « When YOU would defeat Skadihr » : le joueur qui la vainc ; `GetInitiator()` leve une AssertionError quand l'effet
        # vient du vilain (vu : degats poses par la regle de debogage), on retombe alors sur le premier joueur.
        joueur = None
        try:
            joueur = message.GetDefeatingPlayer()
        except Exception:
            joueur = None
        if joueur is None:
            joueur = effect.world.GetFirstPlayer()
        message.SetBeInstead(effect)
        this.HealHealth(99, effect)
        from game.effect.rule import GameRule
        sbire_pv = this.printed_health

        def reprendre(allie: 'Any', ancien: 'Any') -> None:
            allie.printed_health = ancien.printed_health
            allie.printed_health_numeral = ancien.printed_health_numeral
            allie.starting_health = ancien.starting_health

        if Faces.TreatAsAlly(this, "tah_hellbender_ally", joueur, GameRule(this), process=reprendre):
            allie = this.card.face
            allie.traits_internal["WARRIORS THREE"] = [allie]
            allie.traits_internal["ASGARD"] = [allie]
            allie.GainAttackConsequentialDamage(2, effect)
            allie.GainThwartConsequentialDamage(2, effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, "This", devient_allie),
    ]
