from . import *

# In Cold Blood

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed (Alter-Ego): If The Lizard is in play, discard 1 card
        # at random from your hand. »
        if not Worlds.FindCardOnField(effect, name="The Lizard", card_type=Villain):
            return
        joueur = message.GetToPlayer()
        cartes = joueur.hand_cards.Get()
        if cartes:
            Faces.DiscardAll([Rand.RandomChoice(cartes, effect)], effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed (Hero): The Lizard attacks you. You cannot play events
        # until after that attack resolves. If no attack was made this way, this
        # card gains surge. »
        #
        # `DoAttackYou` porte les deux clauses : `you_cannot_play_event` ferme la
        # fenetre des evenements, `if_no_attack_was_made` rend le deferlement.
        lizard = Worlds.FindCardOnField(effect, name="The Lizard", card_type=Villain)
        if not lizard:
            ThisCardGainSurge(effect, message)
            return
        lizard.CastTo(Enemy).DoAttackYou(
            message.GetToPlayer(),
            effect,
            you_cannot_play_event=True,
            if_no_attack_was_made=lambda: ThisCardGainSurge(effect, message),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            alter_ego
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            heros
        ),
    ]
