from . import *

# Energy Overload
# When Revealed: If you have no cards with a printed [energy] resource in your
#   hand, this card gains surge. Otherwise, for each card with a printed
#   [energy] resource in your hand, choose:
#   - Discard that card.  - Stun a character you control.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        energies = [f for f in joueur.hand_cards.Get() if ClassCard.IsType(f) and f.printed_resource.HasColorPrinted("Y")]
        if not energies:
            ThisCardGainSurge(effect)
            return
        for carte in energies:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(f"Discard {carte.name}", lambda targets, c=carte: Faces.DiscardAll([c], effect)),
                AbilityFactory.ForChoiceAbility(
                    "Stun a character you control",
                    lambda targets: Faces.GiveStatus(targets, "Stunned", effect),
                ).SetTarget("YouControlUnit", canbe_stunned=True),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
