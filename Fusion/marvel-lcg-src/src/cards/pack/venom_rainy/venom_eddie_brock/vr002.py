from . import *

# Bulletproof — custom « Rainy »
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, prevent 2 of that damage and draw 1 card. Then, you may shuffle
#   this card into your deck.

def GetAbilities() -> Sequence['Ability']:

    def bulletproof(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)

        message.PreventDamage(2, effect)
        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

        def remelanger(targets: Sequence['CardFace']) -> None:
            deck = initiator.GetPlayerDeck()
            Faces.ShuffleAllTo([this], deck, effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Shuffle Bulletproof into your deck",
                remelanger,
            ),
        )

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            bulletproof,
            is_from_attack=True,
        ).SetPlay(hero_form_only=True)
        .SetLabel('defense'),
    ]
