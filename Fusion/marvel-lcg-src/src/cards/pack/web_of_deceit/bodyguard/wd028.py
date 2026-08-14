from . import *

# Bodyguard (sbire)

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)

        # « Choose to give the villain a tough status card or heal 4 damage from
        # the villain. If you cannot, put this card into play engaged with you. »
        joueur = message.GetToPlayer()
        villain = Worlds.FindVillain(effect)
        if villain is None:
            joueur.DealEncounterCard(this, effect)
            return

        def donner_tough(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus([villain], "Tough", effect)

        def soigner(targets: Sequence['CardFace']) -> None:
            this.HealthUnits([villain], 4, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Give the villain a tough status card",
                donner_tough,
            ),
            AbilityFactory.ForChoiceAbility(
                "Heal 4 damage from the villain",
                soigner,
            ),
        )

    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
