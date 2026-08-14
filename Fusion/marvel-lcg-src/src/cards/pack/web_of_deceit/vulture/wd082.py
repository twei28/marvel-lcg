from . import *

# Fisk Helicopter

def GetAbilities() -> Sequence['Ability']:

    def defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # « When Defeated: Choose:
        #   • Spend 2 resources of the same type.
        #   • Place 2 threat on a scheme. The defeating player takes 2 indirect
        #     damage. »
        this = effect.this.CastTo(Minion)
        joueur = effect.GetInitiator()

        def menace_et_douleur(cibles: 'Sequence[CardFace]') -> None:
            this.PlaceThreatOnSchemes(cibles, 2, effect)
            joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("2", same_type=True),
                "Spend 2 resources of the same type",
            ),
            AbilityFactory.ForChoiceAbility(
                "Place 2 threat on a scheme, then take 2 indirect damage",
                menace_et_douleur
            ).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
    ]
