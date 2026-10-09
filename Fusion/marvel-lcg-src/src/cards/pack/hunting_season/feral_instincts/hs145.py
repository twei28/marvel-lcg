from . import *

# hs145 Cornered Animal
# When Revealed: You take 1 damage. If the villain has taken 6[per_hero] or more damage,
# choose to either spend an [energy] or take 2 indirect damage. If 12[per_hero] or more,
# choose to either discard a random card from your hand or place 2 threat on the main scheme.

def GetAbilities() -> Sequence['Ability']:

    def acculee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeDamage(this, 1, effect)
        if vilain is None:
            return
        subis = vilain.GetLostHealth()
        par_joueur = Worlds.GetPlayerNumIcon(effect)

        if subis >= 6 * par_joueur:
            def indirect(cibles):
                ident = joueur.GetIdentity()
                if ident is not None:
                    ident.TakeIndirectDamage(this, 2, effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbilityWithCost(Cost("Y")),
                AbilityFactory.ForChoiceAbility("Take 2 indirect damage", indirect),
            )

        if subis >= 12 * par_joueur:
            def defausse(cibles):
                joueur.DiscardRandomHandCards(1, effect)

            def menace(cibles):
                complot = Worlds.FindMainScheme(effect)
                if complot is not None:
                    Faces.PlaceTokensOn([complot], 2, 'threat', effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Discard a random card from your hand", defausse),
                AbilityFactory.ForChoiceAbility("Place 2 threat on the main scheme", menace),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, acculee),
    ]
