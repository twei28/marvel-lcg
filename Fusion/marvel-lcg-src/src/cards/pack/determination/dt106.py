from . import *

# * Captain Universe

def GetAbilities() -> Sequence['Ability']:

    def captain_universe(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player is None:
            return
        # CORRECTIF 20/10/2026 (backlog 13, trouve par l'autoplay du deck de
        # test) : `PreventDamage` n'existe que sur `WhenUnitWouldTakeDamage`
        # (sender_damage.py) ; ici l'appel levait AttributeError, avale par le
        # moteur, et la reduction ne partait jamais. Le message des degats
        # consequents porte `ReduceDamage` (sender_friend.py). « reduce that
        # amount by X » : plafonne aux degats prevus, jamais en dessous de 0.
        valeur = min(len(player.dealt_encounter_cards.Get()), message.will_take_damage)
        if valeur > 0:
            message.ReduceDamage(valeur, effect)

    def check_this(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        return effect.this == message.trigger

    return [
        *Alias(),
        Ability(
            AbilityType.Interrupt,
            Message.WhenAllyWouldTakeConsequentialDamage,
            [check_this],
            captain_universe,
            is_local=True
        ),
    ]
