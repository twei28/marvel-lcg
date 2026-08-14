from . import *

# Falling

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « Peril. When Revealed: Choose:
        #   • Exhaust an AERIAL card you control.
        #   • Discard 3 cards from your hand at random.
        #   • Take 5 damage. »
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()

        aeriennes = CardFinder(trait="AERIAL", canbe_exhaust=True).Checks(
            joueur.GetControlCards())

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust an AERIAL card you control",
                lambda cibles: Faces.ExhaustAll(cibles, effect),
                condition=aeriennes != []
            ).SetTarget(CardFinder(trait="AERIAL", canbe_exhaust=True)),
            AbilityFactory.ForChoiceAbility(
                "Discard 3 cards from your hand at random",
                lambda cibles: joueur.DiscardRandomHandCards(3, effect)
            ),
            AbilityFactory.ForChoiceAbility(
                "Take 5 damage",
                lambda cibles: this.DealDamage([identite], 5, effect)
            ),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
