from . import *

# * Spider-Woman (Charlotte Witter) — custom « Kajislav », minion nemesis
# When Revealed: Choose to either take 2 indirect damage or exhaust your identity.

def GetAbilities() -> Sequence['Ability']:

    def witter(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        player = message.GetToPlayer()
        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 2 indirect damage",
                lambda targets:
                    player.GetIdentity().TakeIndirectDamage(this, 2, effect)
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity",
                lambda targets:
                    Faces.ExhaustAll(targets, effect),
            ).SetTarget("YourIdentity", canbe_exhaust=True),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            witter
        ),
    ]
