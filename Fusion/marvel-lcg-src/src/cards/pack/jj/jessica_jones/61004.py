from . import *
def GetAbilities() -> Sequence['Ability']:
    def big_mistake(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
        player = effect.GetInitiator()
        if alias and alias.GetCounters('evidence') >= 1:
            def boosted(_targets: Sequence['CardFace']):
                alias.RemoveCountersInternal(1, 'evidence', effect)
                from game.element.attack_property import AttackProperty
                def with_overkill(_t: Sequence['CardFace']):
                    this.AttackDamage(effect.targets, 5, effect, property=AttackProperty(overkill=True))
                def with_piercing(_t: Sequence['CardFace']):
                    this.AttackDamage(effect.targets, 5, effect, property=AttackProperty(piercing=True))
                player.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility('Overkill', with_overkill),
                    AbilityFactory.ForChoiceAbility('Piercing', with_piercing),
                )
            def unboosted(_targets: Sequence['CardFace']):
                this.AttackDamage(effect.targets, 3, effect)
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility('Remove 1 evidence counter from Alias Investigations to deal 2 additional damage and gain overkill or piercing', boosted),
                AbilityFactory.ForChoiceAbility('Deal 3 damage', unboosted),
            )
        else:
            this.AttackDamage(effect.targets, 3, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, big_mistake).SetPlay().SetLabel('attack').SetTarget(Enemy)]
