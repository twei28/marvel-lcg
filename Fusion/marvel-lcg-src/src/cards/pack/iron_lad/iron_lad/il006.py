from . import *

# Ion Blast (3/3) — contenu identique a il004, voir ce fichier pour le
# detail du modele repris.

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
