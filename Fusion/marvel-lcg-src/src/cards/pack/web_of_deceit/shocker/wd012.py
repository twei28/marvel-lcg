from . import *

# The Getaway

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        villain = Worlds.FindVillain(effect)

        def soigner(targets: Sequence['CardFace']) -> None:
            if villain:
                this.HealthUnits([villain], 3, effect)
                villain.DoSchemes(joueur, effect)

        def rappeler_les_gants(targets: Sequence['CardFace']) -> None:
            if not Worlds.FindCardOnField(effect, name="Vibro-Shock Gauntlets"):
                ChercherEtReveler(effect, name="Vibro-Shock Gauntlets")

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Heal 3 damage from Shocker. Shocker schemes.",
                soigner,
            ),
            AbilityFactory.ForChoiceAbility(
                "Search for the Vibro-Shock Gauntlets and reveal it.",
                rappeler_les_gants,
            ),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
