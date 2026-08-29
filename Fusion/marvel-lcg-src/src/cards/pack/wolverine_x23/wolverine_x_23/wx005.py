from . import *

# Claw Mastery
# Max 1 per round.
# Hero Action: Until the end of the round, Wolverine gets +2 ATK (and her
#   attacks gain overkill while Honey Badger is in play).
#
# Copie de Claw Mastery (43005). Deux bornes ajoutees : la cible passe par
# « YourIdentity », et la condition d'overkill cherche TA Honey Badger, pas
# celle d'un joueur X-23 assis a cote.


def GetAbilities() -> Sequence['Ability']:

    def claw_mastery(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        for face in effect.targets:
            face.GainUntilRoundEnd(
                effect,
                attack=2
            )

            face.effect.RegisterTemp(
                AbilityFactory.UnitAttackGainKeyword(
                    "This",
                    overkill=True,
                    conditions=[
                        lambda effect, message:
                            TonHoneyBadger(effect) != None
                    ]
                ),
                unregister_after_exec=False,
                until_round_end=True
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            claw_mastery
        ).SetPlay().SetLabel()
        .SetTarget("YourIdentity")
        .MaxOnePerRound(),
    ]
