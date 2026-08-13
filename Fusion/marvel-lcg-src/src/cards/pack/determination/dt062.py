from . import *

# "That All You Got?"

def GetAbilities() -> Sequence['Ability']:

    def that_all_you_got(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.EncounterCard(
            effect, initiator,
            include_discard_pile=False,
            finder=CardFinder(card_type=Attachment),
        )
        if face:
            Faces.LookAt([face], initiator, effect)
            initiator.DrawUp(3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            that_all_you_got
        ).SetPlay(),
    ]
