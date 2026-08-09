from . import *

# Darkforce Channel — custom « DesignHacker »
# Hero Action (attack): Choose up to 3 different enemies. Deal 1 damage to
#   each of them and heal 1 damage from Cloak for each enemy damaged this way.
#   Confuse the villain. Then, if Dagger is in play, stun an enemy.


def GetAbilities() -> Sequence['Ability']:

    def darkforce_channel(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        cibles = list(effect.targets)
        this.DealDamage(cibles, 1, effect)

        identite = initiator.GetIdentity()
        if identite is not None and cibles:
            this.HealthUnits([identite], len(cibles), effect)

        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if vilain:
            Faces.GiveStatus([vilain], "Confused", effect)

        if TrouverDagger(effect) is not None:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy",
                    lambda targets: Faces.GiveStatus(targets, "Stunned", effect),
                ).SetTarget(Enemy, canbe_stunned=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            darkforce_channel,
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy, range=(1, 3)),
    ]
