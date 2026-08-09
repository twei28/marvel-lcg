from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        faces = list(player.GetControlCharacters())
        dense = Worlds.FindCardOnField(effect, name='Dense', card_type=Attachment)
        intangible = Worlds.FindCardOnField(effect, name='Intangible', card_type=Attachment)
        if faces:
            def action(chosen: Sequence['CardFace']):
                target = chosen[0]
                Faces.ExhaustAll([target], effect)
                if dense:
                    this.DealDamage([target], 2, effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Exhaust a character you control', action).SetTarget(faces, range=(1, 1), not_move=True))
        if intangible:
            intangible.card.Flip(effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
