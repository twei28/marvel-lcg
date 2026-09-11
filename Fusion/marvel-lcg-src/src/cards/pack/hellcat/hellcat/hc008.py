from . import *
# Illusion — EVENEMENT, cout 1, [mental]. PSIONIC. TACTIC. x2.
# Action: Choose one:
#   • Heal a friendly character by 1 for each card attached to your identity.
#   • Remove 1 threat from a scheme for each card attached to your identity.
#
# Modele : 45016 Side-by-Side (`ChooseAbilities` + `ForChoiceAbility` avec
# cibles). « friendly character » = identite + allies du joueur
# (`Worlds.GetOnFieldFriendlyCharacters`, restreint au joueur).
# ⚠ « for each card attached to your identity » = les cartes GLISSEES par la
#   mecanique du pack (voir __init__), pas les ameliorations. Zero carte
#   accrochee : la carte se joue et ne fait rien (texte respecte).

def GetAbilities() -> Sequence['Ability']:

    def illusion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        identite = IdentiteDe(effect)
        if joueur is None or identite is None:
            return
        n = len(CartesAttacheesA(identite))
        amis = [u for u in Worlds.GetOnFieldFriendlyCharacters(effect)
                if u.GetControlByPlayer() is joueur]
        manigances = list(Worlds.GetOnFieldSchemes(effect))
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Heal a friendly character by {n}",
                lambda targets: this.HealthUnits(list(targets), n, effect),
            ).SetTarget(amis, range=(1, 1)),
            AbilityFactory.ForChoiceAbility(
                f"Remove {n} threat from a scheme",
                lambda targets: this.RemoveThreatFromSchemes(list(targets), n, effect),
            ).SetTarget(manigances, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            illusion,
        ).SetPlay(),
    ]
