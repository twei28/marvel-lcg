from . import *

# Ion Blast (1/3)
# Hero Action (attack): Deal 2 damage to an enemy. You may discard 5 cards
#   from your deck to deal 6 damage instead.
#
# Choix binaire (pas "jusqu'a 5" : le texte impose exactement 5 ou rien) via
# `initiator.AskChooseOneText(["No", "Yes"], text_list=[...])`, modele du
# choix textuel de dt070.py. Defausse ensuite les 5 cartes du dessus
# (`DiscardDeckTopCards`, pas de choix de carte precise dans le texte
# imprime).

def GetAbilities() -> Sequence['Ability']:

    def ion_blast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        cible = effect.targets[0]

        degats = 2
        choix = initiator.AskChooseOneText(
            ["No", "Yes"],
            text_list=["Deal 2 damage", "Discard 5 cards from your deck to deal 6 damage instead"],
        )
        if choix == "Yes":
            initiator.DiscardDeckTopCards(5, effect)
            degats = 6

        this.DealDamage([cible], degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ion_blast
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, 1)),
    ]
