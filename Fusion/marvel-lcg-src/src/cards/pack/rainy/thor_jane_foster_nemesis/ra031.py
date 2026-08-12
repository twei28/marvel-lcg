from . import *

# Hostile Takeover — custom "Rainy" (némésis de Thor Jane Foster)
# When Revealed: Choose to either discard the support you control with the
# highest cost or take damage equal to its cost (this damage ignores tough
# status cards). If no support was discarded and no damage was taken this
# way, this card gains surge.

def GetAbilities() -> Sequence['Ability']:

    def hostile_takeover(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()

        supports = [x for x in Worlds.FindCardsOnField(effect, card_type=Support)
                    if x.GetControlBy() == player and x.has_printed_cost]
        if not supports:
            this.GainSurge(1, effect)
            return

        highest = max(x.printed_cost.val for x in supports)
        candidates = [x for x in supports if x.printed_cost.val == highest]

        def discard_support(targets: Sequence['CardFace']) -> None:
            Faces.DiscardAll(targets, effect)

        def take_damage(targets: Sequence['CardFace']) -> None:
            # LENIENT : « ignores tough » approximé par piercing (défausse la
            # carte solide avant les dégâts).
            this.DealDamage(
                [player.GetIdentity()], highest, effect,
                property=AttackProperty(piercing=True))

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard the support you control with the highest cost",
                discard_support
            ).SetTarget(candidates),
            AbilityFactory.ForChoiceAbility(
                f"Take {highest} damage (ignores tough)",
                take_damage
            )
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hostile_takeover
        )
    ]
