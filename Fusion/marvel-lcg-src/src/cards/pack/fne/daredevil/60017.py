from . import *
def GetAbilities() -> Sequence['Ability']:
    def billy_club(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        Faces.AddToHand([this], initiator, effect)
        def deal_damage(targets: Sequence['CardFace']):
            this.DealDamage(targets, 1, effect)
        def gain_aerial(targets: Sequence['CardFace']):
            identity = initiator.GetIdentity()
            identity.GainTraitsUntilEndOfRound(['AERIAL'], effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Deal 1 damage to an enemy', deal_damage).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility('Daredevil gains the AERIAL trait until the end of the round', gain_aerial))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached('You', attack=1),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, billy_club)]
