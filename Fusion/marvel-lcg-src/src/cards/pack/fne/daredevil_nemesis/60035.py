from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        initiator = effect.GetInitiator()
        elektra = Worlds.FindCardOnField(effect, name='Elektra', card_type=Ally)
        if not elektra:
            Faces.DiscardAll([this], effect)
            return
        def attach(targets: Sequence['CardFace']):
            this.AttachTo2(elektra, effect)
        def discard(targets: Sequence['CardFace']):
            Faces.DiscardAll([this], effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Attach this card to Elektra', attach),
            AbilityFactory.ForChoiceAbility('Discard this card', discard))
    def sai_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « Boost: If this activation is an attack, it gains piercing. »
        # Modele officiel : Crossfire 04027 (during_attack filtre les attaques).
        message.would_atk_message.GainPiercing(effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(Enemy, highest_atk=True),
            AbilityFactory.UnitAttackGainKeyword(CardFinder(with_attach=True), piercing=True, conditions=[lambda effect, message: (message.attacker == effect.this.bind_face)]),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCostFunc(CostFunc.Spend(Cost('RR'))),
            AbilityFactory.WhenCardBecomeBoost('This', sai_boost, during_attack=True)]
