from . import *

# Burning Rubber
# When Revealed: For each speed counter on the main scheme, choose:
#   • Spend 1 resource of any type.  • Place 1 threat on the main scheme.
# Branche payante offerte seulement si payable (PeutCouvrirLeCout, 60127) ;
# sinon la seconde branche s'impose.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def payable(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("1"))

        def branches() -> Sequence['Ability']:
            return [
                AbilityFactory.ForChoiceAbilityWithCost(Cost("1"), "Spend 1 resource of any type", lambda targets, res: None, conditions=[payable]),
                AbilityFactory.ForChoiceAbility("Place 1 threat on the main scheme", lambda targets: this.PlaceThreatOnSchemes("MainScheme", 1, effect)),
            ]

        PourChaqueCompteurDeVitesse(effect, joueur, branches)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
