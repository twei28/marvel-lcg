from . import *
def GetAbilities() -> Sequence['Ability']:
    def improvisation(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        allies = list(player.allies.Get())
        if allies:
            def action(targets: Sequence['CardFace']):
                Faces.ReadyAll(list(targets), effect)
                this.HealthUnits(list(targets), 2, effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Ready an ally and heal 2 damage from it', action).SetTarget(allies, range=(1, 1), not_move=True))
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.HeroResource, Resources('GG'), for_card=(CardFinder(card_type=Event, trait='ATTACK') | CardFinder(card_type=Event, trait='TACTIC')), is_play_card=True, ex_operation=improvisation)]
