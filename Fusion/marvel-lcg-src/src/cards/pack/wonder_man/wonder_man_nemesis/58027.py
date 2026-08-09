from . import *
def GetAbilities() -> Sequence['Ability']:
    def brother_cost(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        attacker = message.trigger
        player = attacker.GetControlByPlayer()
        if not player:
            return
        hand = list(player.hand_cards.Get())
        if not hand:
            message.SetBeInstead(effect)
            return
        def act(chosen: Sequence['CardFace']):
            Faces.DiscardAll(list(chosen), effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard 1 card from your hand', act).SetTarget(hand, range=(1, 1), not_move=True))
    def check_attacks_grim(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        attacker = message.trigger
        if not (Hero.IsType(attacker) or Ally.IsType(attacker)):
            return False
        grim = Worlds.FindCardOnField(effect, name='Grim Reaper', card_type=Minion)
        return bool(grim) and message.HasTarget(grim)
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, None, brother_cost, conditions=[check_attacks_grim])]
