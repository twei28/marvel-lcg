from . import *

# Always a Bigger Conspiracy — custom « ekAugust »
# When Jessica Jones thwarts a side scheme, she may use her ATK instead of her
#   THW.
# When Defeated: Discard cards from the top of the encounter deck until you
#   discard a side scheme. Reveal that side scheme.

def GetAbilities() -> Sequence['Ability']:

    def use_atk(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        message.UseATKInsteadTHW(effect)

    def est_jessica_jones(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> bool:
        return "Jessica Jones" in message.trigger.name

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        face = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=SchemeSide2,
        )
        if face:
            face.Reveal(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.Interrupt,
            None,
            SchemeSide2,
            use_atk,
            is_basic_thwart=True,
            conditions=[est_jessica_jones],
        ),

        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            when_defeated,
        ),
    ]
