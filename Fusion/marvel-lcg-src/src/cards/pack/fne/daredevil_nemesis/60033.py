from . import *
def GetAbilities() -> Sequence['Ability']:
    def bullseye_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        persona_supports = [x for x in Worlds.FindCardsOnField(effect, card_type=Support, trait='PERSONA') if (x.GetControlBy() == player)]
        def discard_persona(targets: Sequence['CardFace']):
            Faces.DiscardAll(targets, effect)
        def attack_you(targets: Sequence['CardFace']):
            this.DoAttackYou(player, effect)
        choices = []
        if persona_supports:
            choices.append(AbilityFactory.ForChoiceAbility('Discard a PERSONA support you control', discard_persona).SetTarget(persona_supports))
        choices.append(AbilityFactory.ForChoiceAbility('Bullseye attacks you', attack_you))
        player.ChooseAbilities(effect, *choices)
    return [AbilityFactory.WhenThisRevealed(None, bullseye_revealed)]
