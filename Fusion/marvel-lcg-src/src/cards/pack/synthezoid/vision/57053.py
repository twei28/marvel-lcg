from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        upgrades = [f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade) if (f.GetControlByPlayer() == player)]
        intangible = Worlds.FindCardOnField(effect, name='Intangible', card_type=Attachment)
        dense = Worlds.FindCardOnField(effect, name='Dense', card_type=Attachment)
        if upgrades:
            target = upgrades[0]
            if intangible:
                Faces.DiscardAll([target], effect)
            else:
                Faces.ExhaustAll([target], effect)
        if dense:
            dense.card.Flip(effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
