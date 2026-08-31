from . import *

# Wake Thy Power — evenement. SPELL. Cout 1. x2
# Hero Action: Discard the top 2 cards of your deck. For each resource icon
#   discarded this way, do the following:
#   [energy] - Remove 2 threat from a scheme.
#   [mental] - Draw 1 card.
#   [physical] - Heal 2 damage from your hero.
#   [wild] - Choose 1 of the above.
#
# Cartes de reference (RECETTES) : 01050 * Hulk pour la lecture des couleurs
# (`FacesCounter.GetPrintedResources`, accesseurs .y/.b/.r/.g) et an011 pour
# `DiscardDeckTopCards`. Les cibles au choix passent par
# `ChooseAbilities` + `ForChoiceAbility` (08013).
#
# ⚠ « for each resource ICON » : une carte a double icone (Energy « YY »,
# aa007 « GB ») compte DEUX fois — on itere sur les icones, pas les cartes.
# Le [wild] offre le choix D'UNE des trois branches, une fois par icone.

def GetAbilities() -> Sequence['Ability']:

    def wake_thy_power(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        defaussees = initiator.DiscardDeckTopCards(2, effect)
        if not defaussees:
            return
        res = FacesCounter.GetPrintedResources(defaussees)

        def menace(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, 2, effect)

        def branche_energie() -> None:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme", menace,
                ).SetTarget(Scheme2),
            )

        def branche_mental() -> None:
            initiator.DrawUp(1, effect)

        def branche_physique() -> None:
            hero = initiator.GetHero()
            if hero is not None:
                this.HealthUnits([hero], 2, effect)

        for _ in range(res.y):
            branche_energie()
        for _ in range(res.b):
            branche_mental()
        for _ in range(res.r):
            branche_physique()
        for _ in range(res.g):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme", menace,
                ).SetTarget(Scheme2),
                AbilityFactory.ForChoiceAbility(
                    "Draw 1 card",
                    lambda targets: branche_mental(),
                ),
                AbilityFactory.ForChoiceAbility(
                    "Heal 2 damage from your hero",
                    lambda targets: branche_physique(),
                ),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            wake_thy_power
        ).SetPlay(),
    ]
