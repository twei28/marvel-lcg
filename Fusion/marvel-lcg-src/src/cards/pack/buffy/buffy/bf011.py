from . import *

# Watcher's Guidance — SOUTIEN, cout 1, [mental].
# Action: Exhaust Watcher's Guidance → choose: • Remove 1 threat from a scheme. • Deal 1 damage to an enemy. • Heal 1 damage from an identity.
# Any player may trigger this ability.
#
# CARTES DE REFERENCE
#  - `40197` Safehouse : `ChooseAbilities(effect, ForChoiceAbility(..).SetTarget(..), ..)` + `.AnyPlayerCanDoThis()`.
#  - `25008` : `RemoveThreatFromSchemes(effect.targets..)` ; `this.HealthUnits(targets, n, effect)` pour soigner.
#
# TEXTE CONTRE CODE
#  « Action » nue -> les DEUX formes. « a scheme » -> `Scheme2`. « an enemy » -> `Enemy`. « an identity » -> n'importe quelle identite
#    (de n'importe quel joueur), pas seulement la sienne. « choose » -> UNE branche. « Any player may trigger » -> `AnyPlayerCanDoThis`.


def GetAbilities() -> Sequence['Ability']:

    def guidance(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a scheme",
                lambda targets: this.RemoveThreatFromSchemes(targets, 1, effect),
            ).SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                lambda targets: this.DealDamage(targets, 1, effect),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Heal 1 damage from an identity",
                lambda targets: this.HealthUnits(targets, 1, effect),
            ).SetTarget(Identity, canbe_heal=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            guidance,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]
