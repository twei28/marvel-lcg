from . import *

# Pummel

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        cartes = joueur.GetControlCardsByType(upgrade=True, support=True)
        cartes = CardFinder(canbe_discard=True).Checks(cartes)

        def degats(targets):
            # « Take damage equal to either Bebop or Rocksteady's ATK » : le joueur
            # choisit le vilain ; un seul vilain en jeu, pas de question.
            vilains = VilainsEnJeu(effect)
            if not vilains:
                return
            v = vilains[0] if len(vilains) == 1 else joueur.AskChooseFace(
                vilains, effect, prompt="Choose Bebop or Rocksteady")
            if v is not None and v.attack > 0:
                this.DealDamage([identite], v.attack, effect)

        def defausse(targets):
            joueur.DiscardControlCards(effect, upgrade=True, support=True, highest_cost=True)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Take damage equal to either Bebop or Rocksteady's ATK", degats),
            AbilityFactory.ForChoiceAbility("Discard the highest-cost upgrade or support you control", defausse,
                                            condition=bool(cartes)),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
