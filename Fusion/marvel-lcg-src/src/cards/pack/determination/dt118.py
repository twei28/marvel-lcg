from . import *

# * The Peak

def GetAbilities() -> Sequence['Ability']:

    def recuperer_le_compteur(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        this = effect.this.CastTo(Support)
        if this.GetAllCounters() < 6:
            Faces.PlaceCountersOn([this], 1, 'counter', effect)

    def check_a_vous(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> bool:
        this = effect.this.CastTo(Support)
        player = this.GetControlByPlayer()
        return player is not None and message.trigger.GetControlByPlayer() == player

    def the_peak(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)

        valeur = this.GetAllCounters()
        if valeur <= 0:
            return
        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], valeur, effect)
        RepartirLeRetraitDeMenace(this, effect.GetInitiator(), valeur, effect)

    return [
        AbilityFactory.AfterCardRemovedCounter(
            AbilityType.Response,
            None,
            'counter',
            recuperer_le_compteur,
            conditions=[check_a_vous],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            the_peak
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetCostFunc(CostFunc.Discard(from_where=["YourHandCards"])),
    ]
