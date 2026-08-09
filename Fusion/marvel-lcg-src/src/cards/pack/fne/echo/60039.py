from . import *
def GetAbilities() -> Sequence['Ability']:
    def follow_my_lead(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        finder = CardFinder(card_type=Event)
        def check_cost_card(e2: 'Effect', m2: 'Message.WhenCalculateEffectCost') -> bool:
            return finder.Check(m2.check_effect.this)
        def check_play_card(e2: 'Effect', m2: 'Message.WhenPlayerWouldPlayCard') -> bool:
            return finder.Check(m2.play_face)
        def check_player(e2: 'Effect', m2: 'TriggerNonePlayerMessage') -> bool:
            return (player == m2.to_player)
        def update_cost(e2: 'Effect', m2: 'Message.WhenCalculateEffectCost') -> None:
            m2.UpdateCost(-1, e2)
        modify_effects = this.effect.RegisterTemp(AbilityFactory.WhenCalculateEffectCost(AbilityType.Temp0, update_cost, conditions=[check_cost_card, check_player, lambda e2, m2: m2.check_effect.ability.is_play]), unregister_after_exec=False, until_round_end=True)
        def unregister(e2: 'Effect', m2: 'Message2') -> None:
            Effects.UnRegister(modify_effects)
        this.effect.RegisterTemp(Ability(AbilityType.Temp0, Message.WhenPlayerWouldPlayCard, [check_play_card, check_player], unregister), unregister_after_exec=True, until_round_end=True)
    return [AbilityFactory.AfterUnitUseBasicPower(AbilityType.Response, 'This', follow_my_lead)]
