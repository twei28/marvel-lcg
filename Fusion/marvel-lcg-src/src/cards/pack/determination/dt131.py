from . import *

# * Speedball

def GetAbilities() -> Sequence['Ability']:

    def poser_un_ball(effect: 'Effect', message: 'Message.AfterCardReady') -> None:
        this = effect.this.CastTo(Ally)
        if this.GetCounters('ball') < 2:
            Faces.PlaceCountersOn([this], 1, 'ball', effect)

    def reduire_les_degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)
        message.PreventDamage(this.GetCounters('ball'), effect)

    def check_this(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return effect.this == message.trigger

    return [
        AbilityFactory.CardsEnterPlayExhausted("This"),
        AbilityFactory.AfterCardReady(
            AbilityType.Response,
            "This",
            poser_un_ball,
            by_player="You",
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            None,
            reduire_les_degats,
            is_from_attack=True,
            conditions=[check_this],
        ),
    ]
