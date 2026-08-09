from . import *
def GetAbilities() -> Sequence['Ability']:
    def chance_encounter(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=True, include_discard_pile=True, card_type=Ally)
        if face:
            Faces.AddToHand([face], initiator, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=SchemeSide2)),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Interrupt, None, chance_encounter, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)])]
