from . import *

# Spear Thrust (2/2)
# Exemplaire physique 2 de 2, contenu identique a ok008 (voir ce fichier pour
# le detail du modele repris).


def GetAbilities() -> Sequence['Ability']:

    def spear_thrust(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.DealDamage(effect.targets, 4, effect)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def degat_supplementaire(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 1, effect)

        nombre_exhauste = len(effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards)
        for _ in range(nombre_exhauste):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    degat_supplementaire,
                ).SetLabel('attack').SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            spear_thrust,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("YouControlCards", trait="DORA MILAJE", card_type=Ally, range=(0, 3)))
        .SetTarget(Enemy),
    ]
