from . import *

# Savior Complex

def GetAbilities() -> Sequence['Ability']:

    # 60007 (Elektra) porte le meme remplacement, mais sur elle-meme : elle se
    # declare `is_local`. Savior Complex ecoute TOUS les allies de son
    # controleur, d'ou la condition explicite et pas de `is_local`.
    def check_your_ally(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        this = effect.this.CastTo(Support)
        ally = message.trigger.CastTo(Ally)
        return ally.GetControlByPlayer() == this.GetControlByPlayer()

    def savior_complex(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Support)

        message.SetBeInstead(effect)
        hero = this.GetControlByPlayer().GetHero()
        hero.CastTo(Unit2).TakeDamage(this, message.will_take_damage, effect)

    return [
        Ability(
            AbilityType.HeroInterrupt,
            Message.WhenAllyWouldTakeConsequentialDamage,
            [check_your_ally],
            savior_complex
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
