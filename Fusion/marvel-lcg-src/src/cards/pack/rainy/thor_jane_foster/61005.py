from . import *

# Lightning Strike — custom "Rainy"
# Hero Action (attack): Deal 6 damage to an enemy and 1 damage to each enemy
# engaged with you. If you paid for this card using only [energy] resources,
# stun an enemy.

def GetAbilities() -> Sequence['Ability']:

    def lightning_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        this.DealDamage(effect.targets, 6, effect)

        engaged = Worlds.FindCardsOnField(
            effect,
            card_type=Enemy,
            engaged_with=initiator,
        )
        engaged = [x for x in engaged if not x.IsDefeated()]
        if engaged:
            this.DealDamage(engaged, 1, effect)

        # « paid using only energy » : wild compte comme énergie (règle FFG).
        paid = getattr(effect.context, 'paid_this_resources', None)
        if paid and paid.rbyg.OnlyHasColor("Y"):
            # « stun an enemy » : le joueur choisit librement l'ennemi.
            def stun(targets: Sequence['CardFace']) -> None:
                Faces.GiveStatus(targets, "Stunned", effect)

            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy",
                    stun
                ).SetTarget(Enemy)
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lightning_strike
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy)
    ]
