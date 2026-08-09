from . import *

# Heroic Will — custom « DesignHacker »
# Alter-Ego Action: Exhaust Heroic Will -> change your form.
# Hero Action: Exhaust Heroic Will -> ready Agent Anti-Venom.

def GetAbilities() -> Sequence['Ability']:

    def change_form(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        identity = GetAgentAntiVenom(effect)
        if identity is not None:
            # Action d'alter-ego : « change your form » va donc vers le heros.
            identity.ChangeToForm(Hero, effect)

    def ready_hero(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        identity = GetAgentAntiVenom(effect)
        if identity is not None:
            Faces.ReadyAll([identity], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            change_form,
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ready_hero,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
