from . import *

# Scrying Pool — custom "Rainy"
# Hero Action: Exhaust Scrying Pool -> look at the top card of a deck. You
# may discard that card. If a treachery was looked at this way, remove 1
# threat from a scheme. If an event was looked at from a player deck this
# way, that player draws 1 card.

def GetAbilities() -> Sequence['Ability']:

    def scrying_pool(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()

        def look(deck, owner: 'Player|None') -> None:
            faces = initiator.LookAtDeck(deck, 1, effect)
            if not faces:
                return
            face = faces[0]

            initiator.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard that card",
                    lambda targets: Faces.DiscardAll([face], effect)
                )
            )

            if Treachery.IsType(face):
                def remove_threat(targets: Sequence['CardFace']) -> None:
                    this.RemoveThreatFromSchemes(targets, 1, effect)
                initiator.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Remove 1 threat from a scheme",
                        remove_threat
                    ).SetTarget(Scheme2)
                )

            if owner is not None and Event.IsType(face):
                owner.DrawUp(1, effect)

        choices = [
            AbilityFactory.ForChoiceAbility(
                "Look at the top card of the encounter deck",
                lambda targets: look("EncounterDeck", None)
            )
        ]
        for player in list(effect.world.players):
            if player.is_eliminated:
                continue
            choices.append(
                AbilityFactory.ForChoiceAbility(
                    f"Look at the top card of {player.name}'s deck",
                    lambda targets, p=player: look(p.player_deck, p)
                )
            )
        initiator.ChooseAbilities(effect, *choices)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            scrying_pool
        ).SetCostFunc(CostFunc.Exhaust("This"))
    ]
