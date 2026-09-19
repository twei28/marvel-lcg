from . import *

# Chain Lightning
# When Revealed: For each character you control, choose:
#   - Exhaust that character.
#   - Deal 1 damage to that character (3 damage instead if there are any charge
#     counters on Electric Charge). Remove 1 charge counter from Electric Charge.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        for personnage in list(joueur.GetControlCharacters()):
            if not personnage.IsInPlay():
                continue

            def frapper(targets: Sequence['CardFace'], cible=personnage) -> None:
                degats = 3 if Charges(effect) > 0 else 1
                this.DealDamage([cible], degats, effect)
                RetirerCharges(effect, 1)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(f"Exhaust {personnage.name}", lambda targets, cible=personnage: Faces.ExhaustAll([cible], effect)),
                AbilityFactory.ForChoiceAbility(f"Deal damage to {personnage.name}", frapper),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
