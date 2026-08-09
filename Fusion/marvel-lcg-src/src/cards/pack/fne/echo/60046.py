from . import *
def GetAbilities() -> Sequence['Ability']:
    def improvisation(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        face = message.played_face
        if face.HasTrait('ATTACK'):
            identity.HealHealth(1, effect)
        if face.HasTrait('DEFENSE'):
            def remove_threat(targets: Sequence['CardFace']):
                this.RemoveThreatFromSchemes(targets, 1, effect)
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove 1 threat from a scheme', remove_threat).SetTarget(Scheme2, has_threat=True))
        if face.HasTrait('THWART'):
            def deal_damage(targets: Sequence['CardFace']):
                this.DealDamage(targets, 1, effect)
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Deal 1 damage to an enemy', deal_damage).SetTarget(Enemy))
    def check_traits(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        face = message.played_face
        return (face.HasTrait('ATTACK') or (face.HasTrait('DEFENSE') or face.HasTrait('THWART')))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterPlayerPlayedCard(AbilityType.HeroResponse, 'You', CardFinder(card_type=Event), improvisation, conditions=[check_traits])]
