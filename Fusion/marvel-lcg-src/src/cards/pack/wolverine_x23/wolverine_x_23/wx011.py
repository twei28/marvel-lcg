from . import *

# Pain Tolerance
# Response: After you play a Wolverine card (including this one), heal 1
#   damage from your identity.
#
# Copie de Pain Tolerance (43011), sans adaptation : « a Wolverine card » se
# traduit par `card_class="IdentitySpecific"`, qui designe les cartes propres
# a l'identite du joueur, et le declencheur est deja borne a « You ».


def GetAbilities() -> Sequence['Ability']:

    def pain_tolerance(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_class="IdentitySpecific"),
            pain_tolerance
        ).SetTarget("YourIdentity", canbe_heal=True),
    ]
