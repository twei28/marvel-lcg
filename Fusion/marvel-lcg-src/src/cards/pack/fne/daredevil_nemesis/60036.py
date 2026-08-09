from . import *
def GetAbilities() -> Sequence['Ability']:
    def eye_on_the_target(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        candidates = [x for x in Worlds.FindCardsOnField(effect, card_type=Ally) if (x.GetControlBy() == player)]
        candidates += [x for x in Worlds.FindCardsOnField(effect, card_type=Support, trait='PERSONA') if (x.GetControlBy() == player)]
        def remove_from_game(targets: Sequence['CardFace']):
            Faces.RemoveAllFromGame(targets, effect)
        def attack_you(targets: Sequence['CardFace']):
            bullseye = Worlds.FindCardOnField(effect, name='Bullseye', card_type=Minion)
            if bullseye:
                bullseye.DoAttackYou(player, effect)
            else:
                face = Search.EncounterCard(effect, player, include_discard_pile=True, name='Bullseye')
                if face:
                    face.Reveal(player, effect)
        choices = []
        if candidates:
            choices.append(AbilityFactory.ForChoiceAbility('Remove an ally or PERSONA support you control from the game', remove_from_game).SetTarget(candidates))
        choices.append(AbilityFactory.ForChoiceAbility('Bullseye attacks you', attack_you))
        player.ChooseAbilities(effect, *choices)
    return [AbilityFactory.WhenThisRevealed(None, eye_on_the_target)]
