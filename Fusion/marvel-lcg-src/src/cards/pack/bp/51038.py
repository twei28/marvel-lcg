from . import *

# Target Spotter

def GetAbilities() -> Sequence['Ability']:

    def target_spotter(effect: 'Effect', message: 'Message.WhenMinionWouldEngagePlayer') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        this.effect.RegisterTemp(
            AbilityFactory.EnemyCannotActivate(
                AbilityType.Temp0,
                message.minion,
            ),
            unregister_after_exec=False,
            until_phase_end=True
        )

        # FAQ (MC4DB, 29/09/2026) : « Target Spotter interrupts the engagement
        # of that minion and causes it to engage the player using Target
        # Spotter instead » -- le sbire n'engage JAMAIS l'autre joueur. Avant,
        # l'engagement d'origine allait au bout (Quickstrike, « after this
        # engages you »...) puis le sbire etait re-engage APRES l'evenement.
        # `SetBeInstead` arrete la suite de l'engagement d'origine
        # (`Minion.OnEngagePlayer`) ; le nouvel engagement se fait tout de
        # suite, et lui seul se resout.
        initiator = effect.GetInitiator()
        if message.would_engaged_player is not initiator:
            message.SetBeInstead(effect)
            message.minion.EngagePlayer(initiator, effect)


    return [
        AbilityFactory.WhenMinionWouldEngagePlayer(
            AbilityType.Interrupt,
            Minion,
            None,
            target_spotter,
            # conditions=[
            #     lambda effect, message:
            #         effect.this.GetControlByPlayer() != message.would_engaged_player
            # ]
        ).SetCostFunc(CostFunc.Counter("This", 1, 'target')),
    ]

