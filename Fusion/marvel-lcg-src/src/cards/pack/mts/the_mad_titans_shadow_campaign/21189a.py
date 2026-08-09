from . import *
CAPTIVE_IDS = ('21190', '21191', '21192', '21193')
def GetAbilities() -> Sequence['Ability']:
    from cards.database import CardsDB
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        used = set()
        def action(player: 'Player'):
            choices = []
            for card_id in CAPTIVE_IDS:
                if card_id in used:
                    continue
                if Worlds.FindCardOnField(effect, name=CardsDB.FindCardPaper(card_id).name):
                    continue
                def put(card_id: str = card_id, player: 'Player' = player):
                    def run(targets: Sequence['CardFace']):
                        used.add(card_id)
                        card = CardFactory.GenerateCard(card_id, player.additional_discard_pile, effect.world)
                        card.face.CastTo(Ally).PutIntoPlay(player, effect, under_control=True)
                    return run
                choices.append(AbilityFactory.ForChoiceAbility(CardsDB.FindCardPaper(card_id).name, put()))
            if choices:
                player.ChooseAbilities(effect, *choices)
        Players.ForEachPlayer(effect, action)
        this.card.Flip(effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
